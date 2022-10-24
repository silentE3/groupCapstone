'''
cli contains the main group for commands
'''

import click
from app.commands import gen
from app.commands import grouping


@click.group()
def cli():
    '''
    commands for the grouping tool
    '''


cli.add_command(grouping.group)
cli.add_command(gen.gen)
