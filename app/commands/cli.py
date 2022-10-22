'''
cli contains the main group for commands
'''
import imp
import click
from app.commands import gen
from app.commands import grouping

@click.group()
def cli():
    '''
    
    '''

cli.add_command(grouping.group)
cli.add_command(gen.gen)
