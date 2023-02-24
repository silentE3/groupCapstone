'''
verify contains all the commands for verifying the results
of a grouping
'''

import click
from app import config, models
from app.data import load, reporter


@click.command("report")
@click.argument('groupfile', type=click.Path(exists=True), default="output.csv")
@click.argument('surveyfile', type=click.Path(exists=True), default="dataset.csv")
@click.option('-c', '--configfile', type=click.Path(exists=True), show_default=True, default="config.json", help="Enter the path to the config file.")
@click.option('-r', '--reportfile', show_default=True, default="grouping_results_report.xlsx",
              help="Enter the path to the group report output file.")
def report(groupfile: str, surveyfile: str, reportfile: str, configfile: str):
    '''Generate report- Creates a report on the results of the groups that were generated. 
    It uses the raw survey file to verify the data.

    GROUPFILE is the path to the grouped dataset. [default=output.csv]

    SURVEYFILE is path to the raw survey output. [default=dataset.csv]
    '''

    # load config data and survey data reader
    config_data: models.Configuration = config.read_json(configfile)

    # load the survey data
    survey_data = load.read_survey(config_data['field_mappings'], surveyfile)

    groups = load.read_groups(groupfile, survey_data.records)

    click.echo(f'Writing report to: "{reportfile}"')
    reporter.write_report(
        [groups], survey_data, config_data, reportfile)


@click.command("update-report")
@click.argument('reportfile', type=click.Path(exists=True), default="group_report.xlsx")
def update_report(reportfile: str):
    '''
    update-report - reads in a previously generated report and updates it based on changes made to it

    REPORTFILE is the path to the xlsx based report file to read in
    '''

    config_data: models.Configuration = config.read_report_config(reportfile)

    # load the survey data
    survey_data = load.read_report_survey_data(reportfile,
                                               config_data['field_mappings'])

    groups: list[list[models.GroupRecord]] = load.read_report_groups(
        reportfile, survey_data.records)

    click.echo(f'Writing updated report to: "{reportfile}"')
    reporter.write_report(groups, survey_data,
                          config_data, reportfile)
