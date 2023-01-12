'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''

import click
from app import config, core, models, output
from app.data import load, reporter
from app.group import scoring
from app.grouping.grouper_1 import Grouper1
from app.grouping import grouper_2


@click.command("group")
@click.argument('surveyfile', type=click.Path(exists=True), default='dataset.csv')
@click.option('-o', '--outputfile', show_default=False, default=None, help="Enter the path to the output file. [default: <SURVEYFILE>]")
@click.option('-c', '--configfile', show_default=True, default="config.json", help="Enter the path to the config file.", type=click.Path(exists=True))
@click.option('--report/--no-report', show_default=True, default=False, help="Use this option to output a report on the results of the goruping.")
@click.option('-r', '--reportfile', show_default=False, default=None, help="report filename, relies on --report flag being enabled [default: <outputfile>_report.csv]")
@click.option('-a', '--allstudentsfile', help="list of all student ids in class. Ignored if not included")
#pylint: disable=too-many-arguments, too-many-locals
def group(surveyfile: str, outputfile: str, configfile: str, report: bool, reportfile: str, allstudentsfile: str):
    '''Group Users - forms groups for the users from the survey.

    SURVEYFILE is path to the raw survey output. [default=dataset.csv]
    '''

    # Set the default outputfile value to the input file (SURVEYFILE) value (if
    #  an output file value was not specified)
    if outputfile is None:
        outputfile = surveyfile

    config_data: models.Configuration = config.read_json(configfile)

    records: list[models.SurveyRecord] = load.read_survey(
        config_data['field_mappings'], surveyfile)

    if allstudentsfile:
        click.echo(
            f'checking roster for missing students in {allstudentsfile}')
        roster = load.read_roster(allstudentsfile)
        records = load.add_missing_students(
            records, roster, config_data['field_mappings']['availability_field_names'])

    # Perform pre-grouping error checking
    if core.pre_group_error_checking(config_data["target_group_size"], records):
        return  # error found -- don't continue

    # Run grouping algorithms
    click.echo(f'grouping students from {surveyfile}')

    # Determine min and max possible number of groups
    min_max_num_groups: list[int] = core.get_min_max_num_groups(
        records, config_data["target_group_size"])

    ########## Run "first" grouping algorithm ##########

    # Run the grouping algorithm for all possible number of groups while keeping only the best solution found
    best_solution_grouper_1: Grouper1 = __run_grouping_alg_1(
        records, config_data, min_max_num_groups[0], min_max_num_groups[1])

    # Output results
    outputfile_1: str = f'{outputfile.removesuffix(".csv")}_1.csv'
    click.echo(f'writing groups to {outputfile_1}')
    output.GroupingDataWriter(config_data).write_csv(
        best_solution_grouper_1.best_solution_found, outputfile_1)

    ########## Run "second" grouping algorithm ##########

    # Run the grouping algorithm for all possible number of groups while keeping only the best solution found
    best_solution_grouper_2: list[models.GroupRecord] = __run_grouping_alg_2(
        records, config_data, min_max_num_groups[0], min_max_num_groups[1])

    # Output results
    outputfile_2: str = f'{outputfile.removesuffix(".csv")}_2.csv'
    click.echo(f'writing groups to {outputfile_2}')
    output.GroupingDataWriter(config_data).write_csv(
        best_solution_grouper_2, outputfile_2)

    ########## Output solutions report if configured ##########
    if report:
        solutions: list[list[models.GroupRecord]] = [
            best_solution_grouper_1.best_solution_found, best_solution_grouper_2]
        report_filename = f'{outputfile.removesuffix(".csv")}_report.xlsx'
        if reportfile:
            # ensure the report filename ends .xlsx
            report_filename = f'{reportfile.removesuffix(".xlsx")}.xlsx'
        click.echo(f'Writing report to: "{report_filename}"')
        reporter.write_report(
            solutions, config_data, report_filename)


def __run_grouping_alg_1(records: list[models.SurveyRecord], config_data: models.Configuration,
                         min_num_groups: int, max_num_groups: int) -> Grouper1:
    best_solution_found: Grouper1 = Grouper1(records, config_data, 0)
    for num_groups in range(min_num_groups, max_num_groups + 1):
        grouper = Grouper1(records, config_data, num_groups)
        grouper.create_groups()
        if (num_groups == min_num_groups or
            (best_solution_found.best_solution_score <= grouper.best_solution_score) or
            (best_solution_found.best_solution_score == grouper.best_solution_score) and
                (scoring.standard_dev_groups(best_solution_found.best_solution_found, best_solution_found.scoring_vars) >=
                    scoring.standard_dev_groups(grouper.best_solution_found, grouper.scoring_vars))):
            best_solution_found = grouper
    return best_solution_found


def __run_grouping_alg_2(records: list[models.SurveyRecord], config_data: models.Configuration,
                         min_num_groups: int, max_num_groups: int) -> list[models.GroupRecord]:

    # Additional pre-processing: rank students based on their availability and num of people they are compatible with
    grouper_2.rank_students(records)

    best_solution_found: list[models.GroupRecord] = []
    score: float = 0
    for num_groups in range(min_num_groups, max_num_groups + 1):
        grouper2 = grouper_2.Grouper2(records, config_data, num_groups)
        group_result = grouper2.group_students()
        if grouper2.grade_groups() > score or num_groups == min_num_groups:
            score = grouper2.grade_groups()
            best_solution_found = group_result
    return best_solution_found
