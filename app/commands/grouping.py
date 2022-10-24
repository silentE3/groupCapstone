'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''
import os
import click
from app.data_classes.survey_data import SurveyData
from app.file import read_config, read_dataset


@click.command("group")
@click.option('--datafile', default="dataset.csv", help="Enter the path to the data file.")
@click.option('--outputfile', default="output.csv", help="Enter the path to the output file.")
@click.option('--configfile', default="config.json", help="Enter the path to the config file.")
def group(datafile: str, outputfile: str, configfile: str):
    '''
    commands for reading input and config
    '''

    if not os.path.exists(datafile):
        raise click.BadOptionUsage('--datafile',
                                   f'no datafile found in the given path: "{datafile}"')

    if not os.path.exists(configfile):
        raise click.BadOptionUsage(
            '--configfile', f'no config file found in the given path "{configfile}"')

    config_data = read_config.read_config_json(configfile)
    reader = read_dataset.SurveyDataReader(config_data)

    data = reader.load(datafile)

    row: SurveyData
    for row in data:
        print(row.student_id)
        print(row.availability)
        print(row.disliked_students)
        print(row.preferred_students)

    print(outputfile)
