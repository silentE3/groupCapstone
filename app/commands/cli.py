'''
cli contains the main group for commands
'''

import click
from app.commands import generate, group, verify



@click.group()
def cli():
    '''
    commands for the grouping tool
    '''


cli.add_command(group.group)
cli.add_command(generate.gen)
cli.add_command(verify.verify)
