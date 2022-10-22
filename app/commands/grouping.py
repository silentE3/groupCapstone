'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''
import click


@click.group("group")
@click.option('--datafile', default="dataset.csv", help="Enter the path to the data file.")
@click.option('--configfile', default="config.json", help="Enter the path to the config file.")
def group(datafile: str, configfile: str):
    '''
    commands for reading input and config
    '''
