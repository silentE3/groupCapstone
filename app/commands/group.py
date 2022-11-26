'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''

import click

from app import algorithm, core, models, config, output
from app.group import validate
from app.data import load


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

    records: list[models.SurveyRecord] = load.read_survey(config_data['field_mappings'], surveyfile)

    # loop through the data and if they don't match any availability, set them to be a wildcard
    for record in records:
        if algorithm.total_availability_matches(record, records) == 0:
            print(f"found no matching availability for: {record.student_id}")
            record.availability = set_avail(record)
    algorithm.rank_students(records)
    # Perform pre-grouping error checking
    alg = algorithm.Grouper(records, config_data['target_group_size'], config_data['grouping_passes'])

    click.echo(f'grouping students from {surveyfile}')
    groups = alg.group_students()
    click.echo(f'writing groups to {outputfile}')
    output.GroupingDataWriter(config_data).write_csv(groups, outputfile)

    if verify:
        report = f'{outputfile.removesuffix(".csv")}_report.xlsx'
        if reportfile:
            report = reportfile

        click.echo(f'writing report to {report}')
        core.write_report(groups, config_data, report)


def set_avail(student: models.SurveyRecord):
    '''
    sets the availability
    '''
    avail = {}
    for key in student.availability:
        avail[key] = validate.WEEK_DAYS

    return avail
