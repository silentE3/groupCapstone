'''
cli contains the main group for commands
'''


import click
from app.commands import generate, group, report


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
    commands = {
        'group': group.group,
        'generate': generate.generate
    }

    command_names = list(commands.keys())
    click.echo('Available commands:')
    for name in command_names:
        click.echo(f'* {name}')
    selected_command = click.prompt('Select a command to run', type=click.Choice(command_names))

    match selected_command:
        case 'group':
            surveyfile = click.prompt('Enter the path to the survey file', default='dataset.csv')
            configfile = click.prompt('Enter the path to the config file', default='config.json', show_default=True)
            roster = click.confirm('Do you want to include a class roster with students who did not fill out the survey?')
            if roster:
                allstudentsfile = click.prompt('Enter the path to the file containing all student IDs', default=None,
                                               show_default=False)
            else:
                allstudentsfile = None
            commands[selected_command](surveyfile, configfile, allstudentsfile)
        case 'gen':
            '''get arguments and run generate'''

        case 'update-report':
            '''get arguments and run update_report'''

        case _:
            commands[selected_command]()


cli.add_command(group.group)
cli.add_command(generate.gen)
cli.add_command(report.report)
cli.add_command(report.update_report)

if __name__ == '__main__':
    cli()
