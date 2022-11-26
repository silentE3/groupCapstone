'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''

import click

from app import algorithm, models, config, output
from app.data import load, reporter


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

    records: list[models.SurveyRecord] = load.read_survey(config_data['field_mappings'], surveyfile)

    # loop through the data and if they don't match any availability, set them to be a wildcard
    algorithm.rank_students(records)
    # Perform pre-grouping error checking
    alg = algorithm.Grouper(records, config_data['target_group_size'], config_data['grouping_passes'])

    click.echo(f'grouping students from {surveyfile}')
    groups = alg.group_students()
    click.echo(f'writing groups to {outputfile}')
    output.GroupingDataWriter(config_data).write_csv(groups, outputfile)

    if report:
        report_filename = f'{outputfile.removesuffix(".csv")}_report.xlsx'
        if reportfile:
            report_filename = reportfile
        click.echo(f'Writing report to: "{report_filename}"')
        reporter.write_report(
            groups, config_data, report_filename)
