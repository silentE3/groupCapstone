'''
cli contains the main group for commands
'''

import click
from app.commands import generate, group, report


@click.group()
def cli():
    '''
    commands for the grouping tool
    '''


cli.add_command(group.group)
cli.add_command(generate.gen)
cli.add_command(report.report)
cli.add_command(report.update_report)
