'''
verify contains all the commands for verifying the results
of a grouping
'''

import click
from app import config, models, app
from app.grouping import randomizer


@click.command("verify")
@click.argument('surveyfile', type=click.Path(exists=True), default="dataset.csv")
@click.argument('groupfile', type=click.Path(exists=True), default="output.csv")
@click.option('-c', '--configfile', type=click.Path(exists=True), show_default=True, default="config.json", help="Enter the path to the config file.")
@click.option('-r', '--reportfile', show_default=True, default="grouptreport.xlsx",
              help="Enter the path to the group report output file.")
def verify(surveyfile: str, groupfile: str, reportfile: str, configfile: str):
    '''Verify groups- verifies the groups that were generated. It uses the raw survey file to verify the data.

    SURVEYFILE is path to the raw survey output. [default=dataset.csv]

    GROUPFILE is the path to the grouped dataset. [default=output.csv]
    '''

    # load config data and survey data reader
    config_data: models.Configuration = config.read_json(configfile)

    application = app.Application(config_data, randomizer.RandomGrouper())

    records = application.read_survey(surveyfile)

    # redefine the reader and read in the grouping data
    groups = application.read_groups(groupfile)

    # create the verifier and run the verification
    application.verify_groups(records, groups, reportfile)
