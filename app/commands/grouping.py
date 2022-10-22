'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''
import click
from app.file import read_config, read_dataset


@click.command("group")
@click.option('--datafile', default="dataset.csv", help="Enter the path to the data file.")
@click.option('--outputfile', default="output.csv", help="Enter the path to the output file.")
@click.option('--configfile', default="config.json", help="Enter the path to the config file.")
def group(datafile: str, outputfile: str, configfile: str):
    '''
    commands for reading input and config
    '''
    config_data = read_config.read_config_json(configfile)
    surveys = read_dataset.load_survey_data_csv(datafile, config_data)
    print(f"Surveys loaded: {len(surveys)}.")
    print(surveys)
    print(outputfile)
