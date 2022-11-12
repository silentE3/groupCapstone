'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''

import click

from app import models
from app import app
from app import config
from app.grouping import randomizer


@click.command("group")
@click.argument('surveyfile', type=click.Path(exists=True), default='dataset.csv')
@click.option('-o', '--outputfile', show_default=True, default="output.csv", help="Enter the path to the output file.")
@click.option('-c', '--configfile', show_default=True, default="config.json", help="Enter the path to the config file.", type=click.Path(exists=True))
@click.option('--verify/--no-verify', show_default=True, default=False, help="Use this option to add verification reporting to the data.")
@click.option('-r', '--reportfile', show_default=True, help="report filename, relies on --verify flag being enabled")
def group(surveyfile: str, outputfile: str, configfile: str, verify: bool, reportfile: str):
    '''Group Users - forms groups for the users from the survey.

    SURVEYFILE is path to the raw survey output. [default=dataset.csv]
    '''

    config_data: models.Configuration = config.read_json(configfile)

    application = app.Application(config_data, randomizer.RandomGrouper())

    records = application.read_survey(surveyfile)
    click.echo(f'grouping students from {surveyfile}')
    groups = application.group_students(records)
    click.echo(f'writing groups to {outputfile}')
    application.write_groups(groups, outputfile)

    if verify:
        report = f'{outputfile.removesuffix(".csv")}_report.xlsx'
        if reportfile:
            report = reportfile

        click.echo(f'writing report to {report}')
        application.write_report(groups, report)
