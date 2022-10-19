'''
cli contains the main group for commands
'''
import click
from app.commands import gen

@click.group()
def cli():
    '''
    cli is the main group for all commands
    '''

cli.add_command(gen.gen)
