'''
cli contains the main group for commands
'''
<<<<<<< .merge_file_C4KOEi
import click
from app.commands import gen
=======

import click
from app.commands import gen
from app.commands import grouping

>>>>>>> .merge_file_D4dxZH

@click.group()
def cli():
    '''
<<<<<<< .merge_file_C4KOEi
    cli is the main group for all commands
    '''

=======
    commands for the grouping tool
    '''


cli.add_command(grouping.group)
>>>>>>> .merge_file_D4dxZH
cli.add_command(gen.gen)
