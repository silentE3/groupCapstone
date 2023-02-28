'''
cli contains the main group for commands
'''


import click
from app.commands import generate, group, report
from importlib import import_module


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    '''
    commands for the grouping tool
    '''
    # If no subcommand is provided, invoke the guide command
    if ctx.invoked_subcommand is None:
        ctx.invoke(guide)

@cli.command()
def guide():
    '''
    guide command
    '''
    command_names = ['group', 'generate', 'report', 'update_report']
    click.echo('Available commands:')
    for name in command_names:
        click.echo(f'* {name}')
    selected_command = click.prompt('Select a command to run', type=click.Choice(command_names))
    # Import the selected command module
    module = import_module(f'app.commands.{selected_command}')
    # Invoke the selected command
    ctx = click.get_current_context()
    ctx.invoke(getattr(module, selected_command))

if __name__ == '__main__':
    cli()