'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''

import click

from app import app, algorithm, models, config
from app.grouping import randomizer
from app.group import validate


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

    non_matching: list[models.SurveyRecord] = []
    for idx, record in enumerate(records):
        if algorithm.total_availability_matches(record, records) == 0:
            record.availability = set_avail(record)
            non_matching.append(records[idx])
    algorithm.rank_students(records)
    # filter out any that don't match first

    algorithm.rank_students(records)

    alg = algorithm.Algorithm(records)

    click.echo(f'grouping students from {surveyfile}')
    groups = alg.group_students()
    click.echo(f'writing groups to {outputfile}')
    application.write_groups(groups, outputfile)

    if verify:
        report = f'{outputfile.removesuffix(".csv")}_report.xlsx'
        if reportfile:
            report = reportfile

        click.echo(f'writing report to {report}')
        application.write_report(groups, report)


def set_avail(student: models.SurveyRecord):
    '''
    sets the availability
    '''
    avail = {}
    for key in student.availability:
        avail[key] = validate.WEEK_DAYS

    return avail
