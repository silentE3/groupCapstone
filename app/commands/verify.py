'''
verify contains all the commands for verifying the results
of a grouping
'''
import os
import click
from app.file import read_grouping, verify_grouping
from app import config, load
from app import models

@click.command("verify")
@click.option('--datafile', default="dataset.csv", help="Enter the path to the original data file.")
@click.option('--groupfile', default="output.csv", help="Enter the path to the grouping data file.")
@click.option('--tallyfile', default="grouptally.csv", help="Enter the path to the group tally output file.")
@click.option('--configfile', default="config.json", help="Enter the path to the config file.")
# pylint: disable=duplicate-code
def verify(datafile: str, groupfile: str, tallyfile: str, configfile: str):
    '''
    runs the verification functionality
    '''

    if not os.path.exists(datafile):
        raise click.BadOptionUsage('--datafile',
                                   f'no datafile found in the given path: "{datafile}"')

    if not os.path.exists(groupfile):
        raise click.BadOptionUsage('--groupfile',
                                   f'no grouping data file found in the given path: "{groupfile}"')

    if not os.path.exists(configfile):
        raise click.BadOptionUsage(
            '--configfile', f'no config file found in the given path "{configfile}"')

    # load config data and survey data reader
    config_data: models.Configuration = config.read_json(configfile)
    reader = load.SurveyDataReader(config_data['field_mappings'])

    data = reader.load(datafile)

    # redefine the reader and read in the grouping data
    reader = read_grouping.GroupingDataReader()
    grouping = reader.load(groupfile)

    # create the verifier and run the verification
    verifier = verify_grouping.VerifyGrouping(config_data)
    verifier.verify(data, grouping, tallyfile)
