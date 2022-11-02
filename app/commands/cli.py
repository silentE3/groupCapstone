'''
cli contains the main group for commands
'''

import click
from app.commands import gen
from app.commands import group
from app.commands import verify


@click.group()
def cli():
    '''
    commands for the grouping tool
    '''


cli.add_command(group.group)
cli.add_command(gen.gen)
cli.add_command(verify.verify)
