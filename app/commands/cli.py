'''
cli contains the main group for commands
'''


import re
import sys

import click
import xlsxwriter
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
        'update report': report.update_report,
        'create report': report.report,
        'quit': quitter
    }

    command_names = list(commands.keys())
    click.echo('Available commands:')
    for name in command_names:
        click.echo(f'* {name}')
    selected_command = click.prompt('Select a command to run', type=click.Choice(command_names))
    args = []
    match selected_command:
        case 'group':
            surveyfile = click.prompt('Enter the path to the survey file',
                                      default='dataset.csv')
            configfile = click.prompt('Enter the path to the config file',
                                      default='config.json', show_default=True)
            has_report = click.confirm('Do you already have a report file you want to change?')
            if has_report:
                reportfile = click.prompt('Enter the path to the existing report file (.xlsx)', default=None,
                                               show_default=False)
            else:
                reportfile = None
            roster = click.confirm('Do you want to include a class roster with students who did not fill out the survey?')
            if roster:
                allstudentsfile = click.prompt('Enter the path to the file containing all student IDs (.csv)', default=None,
                                               show_default=False)
            else:
                allstudentsfile = None
            args = [surveyfile, configfile, reportfile, allstudentsfile]

        case 'update report':
            reportfile = click.prompt('Enter the path to the existing report file',
                                      default='dataset_report.xlsx', show_default=False)
            args = [reportfile]

        case 'create report':
            groupfile = click.prompt('Enter the path to the grouping file',
                                     default='output.csv', show_default=True)
            surveyfile = click.prompt('Enter the path to the raw survey file',
                                      default='dataset.csv', show_default=True)
            configfile = click.prompt('Enter the path to the config file',
                                      default='config.json', show_default=True)
            has_report = click.confirm('Do you already have a report file you want to change?')
            if has_report:
                reportfile = click.prompt('Enter the path to the existing report file (.xlsx)', default=None,
                                          show_default=False)
            else:
                group_file_name = re.search(r'\w+|\d+', groupfile).group()
                workbook = xlsxwriter.Workbook(f'{group_file_name}_report.xlsx')
                workbook.close()
                reportfile = f'{group_file_name}_report.xlsx'
            args = [groupfile, surveyfile, reportfile, configfile]
        case 'end':
            quitter()
    commands[selected_command].callback(*args)


def quitter():
    '''quits the program if the user types quit'''
    sys.exit(0)


cli.add_command(report.report)
cli.add_command(group.group)
cli.add_command(generate.gen)
cli.add_command(report.update_report)

if __name__ == '__main__':
    cli(None)
