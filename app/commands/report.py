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

    # redefine the reader and read in the grouping data
    groups = load.read_groups(groupfile, survey_data)

    click.echo(f'Writing report to: "{reportfile}"')
    reporter.write_report(
        [groups], config_data, reportfile)


@click.command("read-report")
@click.argument('reportfile', type=click.Path(exists=True), default="group_report.xlsx")
def read_report(reportfile: str):
    '''
    read report- reads in a previously generated report
    
    REPORTFILE is the path to the xlsx based report file to read in
    '''
    _ = load.read_report(reportfile)
    