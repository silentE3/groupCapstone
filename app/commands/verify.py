'''
verify contains all the commands for verifying the results
of a grouping
'''
import os
import click
from app import config, models
from app.data import load
from app.group import verify as verify_group

@click.command("verify")
@click.option('-d', '--datafile', show_default=True, default="dataset.csv", help="Enter the path to the original data file.")
@click.option('-g', '--groupfile', show_default=True, default="output.csv", help="Enter the path to the grouping data file.")
@click.option('-r', '--groupreport', show_default=True, default="grouptreport.xlsx", help="Enter the path to the group report output file.")
@click.option('-c', '--configfile', show_default=True, default="config.json", help="Enter the path to the config file.")
# pylint: disable=duplicate-code
def verify(datafile: str, groupfile: str, groupreport: str, configfile: str):
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
    reader = load.GroupingDataReader()
    grouping = reader.load(groupfile)

    # create the verifier and run the verification
    verifier = verify_group.VerifyGrouping(config_data)
    verifier.verify(data, grouping, groupreport)
