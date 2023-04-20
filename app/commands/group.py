'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''
from pathlib import Path
from concurrent.futures import as_completed, wait, ProcessPoolExecutor, Future
from multiprocessing import synchronize, Event, current_process
from multiprocessing.managers import BaseManager
import signal
import sys
import click
from app import config, core, models
from app.data import load, reporter
from app.group import scoring
from app.grouping.grouper_1 import Grouper1
from app.grouping import grouper_2, printer


class GroupingManager(BaseManager):
    '''
    A custom version of the BaseManager class so that we can register
     the necessary shared class(es) for the grouping process.
    '''


@click.command("group")
@click.argument('surveyfile', type=click.Path(exists=True), default='dataset.csv')
@click.option('-c', '--configfile', show_default=True, default="config.json", help="Enter the path to the config file.", type=click.Path(exists=True))
@click.option('-r', '--reportfile', show_default=False, default=None,
              help="report filename, relies on --report flag being enabled [default: <surveyfile>_report.csv]")
@click.option('-a', '--allstudentsfile', help="list of all student ids in class. Ignored if not included")
def group(surveyfile: str, configfile: str, reportfile: str, allstudentsfile: str):
    '''Group Users - forms groups for the users from the survey.

    SURVEYFILE is path to the raw survey output. [default=dataset.csv]
    '''
    try:
        ########## Determine Output Filenames ##########
        report_filename: str = __report_filename(surveyfile, reportfile)

        ########## Load the config data ##########
        config_data: models.Configuration = config.read_json(configfile)

        ########## Load the survey data ##########
        survey_data: models.SurveyData = load.read_survey(config_data['field_mappings'], surveyfile)

        ########## Load the class roster data, if applicable ##########
        if allstudentsfile:
            click.echo(
                f'checking roster for missing students in {allstudentsfile}')
            survey_data.records = load.match_survey_to_roster(survey_data.records,
                                                              load.read_roster(allstudentsfile), config_data['field_mappings']['availability_field_names'])
        ########## Grouping ##########

        # Perform pre-grouping error checking
        if core.pre_group_error_checking(config_data["target_group_size"], config_data["target_plus_one_allowed"],
                                         config_data["target_minus_one_allowed"], survey_data.records):
            return  # error found -- don't continue

        # Run grouping algorithms
        click.echo(f'grouping students from {surveyfile}')

        ########################################################################################
        # NOTE: We're no longer doing this (getting a "true" min and max group size). The sponsor
        #  has decided that she would prefer it if the algorithms adhere to the target size to
        #  the extent possible, which means there will only be one "proper" number of groups.

        # Determine min and max possible number of groups
        # min_max_num_groups: list[int] = core.get_min_max_num_groups(
        #    survey_data.records,
        #    config_data["target_group_size"],
        #    config_data["target_plus_one_allowed"],
        #    config_data["target_minus_one_allowed"])
        ########################################################################################
        num_groups: int = core.get_num_groups(survey_data.records,
                                              config_data["target_group_size"],
                                              config_data["target_plus_one_allowed"],
                                              config_data["target_minus_one_allowed"])
        min_max_num_groups: list[int] = [num_groups, num_groups]

        ########## Run both grouping algorithms in parallel via multiprocessing ##########
        best_solutions: list[list[models.GroupRecord]] = __run_grouping_algs(
            survey_data, config_data, min_max_num_groups)

        ########## Output solutions report if configured ##########
        click.echo(f'Writing report to: {report_filename}')
        reporter.write_report(best_solutions, survey_data,
                              config_data, report_filename)

    except ValueError as value_error:
        print(
            f"ValueError: {value_error}\n**Check the paths to the input files, if those are ok, then check them for errors**")
        sys.exit(1)

    except AttributeError as attribute_error:
        print(f"AttributeError: {attribute_error}\n**Check the input files for errors**")
        sys.exit(1)


def __run_grouping_algs(survey_data: models.SurveyData, config_data: models.Configuration, min_max_num_groups: list[int]) -> list[list[models.GroupRecord]]:
    GroupingManager.register('GroupingConsolePrinter',
                             printer.GroupingConsolePrinter)
    GroupingManager.register('Event',
                             Event)

    #pylint: disable=no-member
    with GroupingManager() as grouping_manager:
        managed_grouping_vars: models.ManagedGroupingVars = models.ManagedGroupingVars(
            grouping_manager.Event(), grouping_manager.GroupingConsolePrinter())

        futures: list[Future] = []

        # Allow keyboard interrupt to cleanly cancel the grouping process while
        # grouping processes are in progress

        def interrupt_handler(_, __):
            if not current_process().name == 'MainProcess':
                return
            managed_grouping_vars.grouping_console_printer.print('Cancelling grouping...')
            managed_grouping_vars.grouping_cancel_event.set()

            _, not_done = wait(futures, timeout=0)

            counter: int = 0
            while not_done:
                managed_grouping_vars.grouping_console_printer.print(
                    "Working on cancelling the grouping process cleanly... " + str(counter))
                _, not_done = wait(not_done, timeout=1)
                counter += 1

            managed_grouping_vars.grouping_console_printer.print("Grouping process cancelled successfully.")
            print("\n")
            sys.exit(1)
        signal.signal(signal.SIGINT, interrupt_handler)

        with ProcessPoolExecutor(max_workers=2) as executor:

            ########## Launch "first" grouping algorithm ##########
            # Run the grouping algorithm for all possible number of groups while keeping only the best solution found
            best_solution_grouper_1: Grouper1 = Grouper1(
                survey_data.records, config_data, 0, managed_grouping_vars.grouping_console_printer)
            futures.append(
                executor.submit(__run_grouping_alg_1, survey_data.records,
                                config_data, min_max_num_groups[0],
                                min_max_num_groups[1],
                                managed_grouping_vars))

            ########## Launch "second" grouping algorithm ##########
            # Run the grouping algorithm for all possible number of groups while keeping only the best solution found
            best_solution_grouper_2: list[models.GroupRecord] = []
            futures.append(
                executor.submit(__run_grouping_alg_2, survey_data.records,
                                config_data, min_max_num_groups[0],
                                min_max_num_groups[1], managed_grouping_vars))

            _, not_done = wait(futures, timeout=0)

            while not_done:
                _, not_done = wait(not_done, timeout=1)

            for future in as_completed(futures):
                if isinstance(future.result(), Grouper1):
                    best_solution_grouper_1 = future.result()

                else:
                    best_solution_grouper_2 = future.result()

        return [best_solution_grouper_1.best_solution_found, best_solution_grouper_2]


def __run_grouping_alg_1(records: list[models.SurveyRecord], config_data: models.Configuration,
                         min_num_groups: int, max_num_groups: int, managed_grouping_vars: models.ManagedGroupingVars) -> Grouper1:

    best_solution_found: Grouper1 = Grouper1(
        records, config_data, 0, managed_grouping_vars.grouping_console_printer)

    # Use multiprocessing to execute the grouping in parallel when there are multiple options for
    # the number of groups.
    no_finished_runs: bool = True
    with ProcessPoolExecutor() as executor:
        futures: list[Future] = []
        for num_groups in range(min_num_groups, max_num_groups + 1):
            grouper = Grouper1(records, config_data,
                               num_groups, managed_grouping_vars.grouping_console_printer)
            futures.append(
                executor.submit(grouper.create_groups, managed_grouping_vars.grouping_cancel_event))

        _, not_done = wait(futures, timeout=0)

        while not_done:
            _, not_done = wait(not_done, timeout=1)
            if managed_grouping_vars.grouping_cancel_event.is_set():
                for future in futures:
                    future.cancel()
                return best_solution_found

        use_alternative_scoring: bool = config_data['prioritize_preferred_over_availability']
        for future in as_completed(futures):
            grouper = future.result()
            if (no_finished_runs or
                (best_solution_found.best_solution_score <= grouper.best_solution_score) or
                (best_solution_found.best_solution_score == grouper.best_solution_score) and
                    (scoring.standard_dev_groups(best_solution_found.best_solution_found, best_solution_found.scoring_vars, use_alternative_scoring) >=
                        scoring.standard_dev_groups(grouper.best_solution_found, grouper.scoring_vars, use_alternative_scoring))):
                best_solution_found = grouper
            no_finished_runs = False
    return best_solution_found


def __run_grouping_alg_2(records: list[models.SurveyRecord], config_data: models.Configuration,
                         min_num_groups: int, max_num_groups: int, managed_grouping_vars: models.ManagedGroupingVars) -> list[models.GroupRecord]:

    # Additional pre-processing: rank students based on their availability and num of people they are compatible with
    grouper_2.rank_students(records)
    best_solution_found: list[models.GroupRecord] = []
    best_score: float = 0
    with ProcessPoolExecutor() as executor:
        exec_results = {executor.submit(run_grouper_2, records, config_data, num_groups,
                                        managed_grouping_vars.grouping_console_printer,
                                        managed_grouping_vars.grouping_cancel_event):
                        num_groups for num_groups in range(min_num_groups, max_num_groups + 1)}

        _, not_done = wait(exec_results, timeout=0)

        while not_done:
            _, not_done = wait(not_done, timeout=1)
            if managed_grouping_vars.grouping_cancel_event.is_set():
                for future in exec_results:
                    future.cancel()
                return best_solution_found

        for idx, future in enumerate(as_completed(exec_results)):
            grouper = future.result()
            score = grouper.grade_groups()
            if score > best_score or idx == 0:
                best_score = score
                best_solution_found = grouper.groups

        return best_solution_found


def run_grouper_2(records, config_data, num_groups, grouping_console_printer, cancel_event: synchronize.Event):
    '''
    runs grouper 2 with the given number of groups
    '''
    grouping_console_printer.print(
        'running grouper 2 with ' + str(num_groups) + ' groups')
    grouper2 = grouper_2.Grouper2(
        records, config_data, num_groups, grouping_console_printer)
    grouper2.group_students(cancel_event)
    return grouper2


def __report_filename(surveyfile: str, reportfile: str) -> str:

    # Set the default output filename values per the input filename (SURVEYFILE) value (if
    if reportfile is None:
        # the default report filename is based upon the surveyfile filename
        reportfile = f'{surveyfile.removesuffix(".csv")}_report'

    # ensure the report filename ends .xlsx
    report_filename: str = f'{reportfile.removesuffix(".xlsx")}.xlsx'

    # Append integer value to avoid output file overwriting
    if Path('./' + report_filename).is_file():
        print(report_filename + " already exists...", end='')
        append_value: int = 1
        new_filename: str = report_filename.removesuffix(
            '.xlsx') + '_' + str(append_value) + '.xlsx'
        while (Path('./' + new_filename).is_file()):
            append_value += 1
            new_filename = report_filename.removesuffix(
                '.xlsx') + '_' + str(append_value) + '.xlsx'
        print('available filename: ' + new_filename)
        report_filename = new_filename

    print()

    return report_filename
