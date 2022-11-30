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
@click.option('-o', '--outputfile', show_default=True, default="output.csv", help="Enter the path to the output file.")
@click.option('-c', '--configfile', show_default=True, default="config.json", help="Enter the path to the config file.", type=click.Path(exists=True))
@click.option('--report/--no-report', show_default=True, default=False, help="Use this option to output a report on the results of the goruping.")
@click.option('-r', '--reportfile', show_default=True, help="report filename, relies on --report flag being enabled")
def group(surveyfile: str, outputfile: str, configfile: str, report: bool, reportfile: str):
    '''Group Users - forms groups for the users from the survey.

    SURVEYFILE is path to the raw survey output. [default=dataset.csv]
    '''

    config_data: models.Configuration = config.read_json(configfile)

    records: list[models.SurveyRecord] = load.read_survey(
        config_data['field_mappings'], surveyfile)
    # Perform pre-grouping error checking
    if core.pre_group_error_checking(config_data["target_group_size"], records):
        return  # error found -- don't continue

    # Run grouping algorithms
    click.echo(f'grouping students from {surveyfile}')

    ########## Run "first" grouping algorithm ##########

    # Determine min and max possible number of groups
    min_max_num_groups: list[int] = core.get_min_max_num_groups(
        records, config_data["target_group_size"])

    # Run the grouping algorithm for all possible number of groups while keeping only the best solution found
    best_solution_found_grouper: Grouper1 = Grouper1(records, config_data, 0)
    for num_groups in range(min_max_num_groups[0], min_max_num_groups[-1] + 1):
        grouper = Grouper1(records, config_data, num_groups)
        grouper.create_groups()
        if (num_groups == min_max_num_groups[0] or
            (best_solution_found_grouper.best_solution_score <= grouper.best_solution_score) or
            (best_solution_found_grouper.best_solution_score == grouper.best_solution_score) and
                (scoring.standard_dev_groups(best_solution_found_grouper.best_solution_found, best_solution_found_grouper.scoring_vars) >=
                    scoring.standard_dev_groups(grouper.best_solution_found, grouper.scoring_vars))):
            best_solution_found_grouper = grouper

    # Output results
    outputfile_1: str = f'{outputfile.removesuffix(".csv")}_1.csv'
    click.echo(f'writing groups to {outputfile_1}')
    output.GroupingDataWriter(config_data).write_csv(
        best_solution_found_grouper.best_solution_found, outputfile_1)

    ########## Run "second" grouping algorithm ##########

    # Additional pre-processing: rank students based on their availability and num of people they are compatible with
    grouper_2.rank_students(records)
    # Perform pre-grouping error checking
    grouper2 = grouper_2.Grouper2(
        records, config_data, config_data['target_group_size'], config_data['grouping_passes'])

    groups = grouper2.group_students()

    # Output results
    outputfile_2: str = f'{outputfile.removesuffix(".csv")}_2.csv'
    click.echo(f'writing groups to {outputfile_2}')
    output.GroupingDataWriter(config_data).write_csv(groups, outputfile_2)

    ########## Output solutions report if configured ##########
    if report:
        solutions: list[list[models.GroupRecord]] = [
            best_solution_found_grouper.best_solution_found, groups]
        report_filename = f'{outputfile.removesuffix(".csv")}_report.xlsx'
        if reportfile:
            report_filename = reportfile
        click.echo(f'Writing report to: "{report_filename}"')
        reporter.write_report(
            solutions, config_data, report_filename)
