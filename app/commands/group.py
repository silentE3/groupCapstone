'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''

import click

from app import config, core, output
from app import models
from app.data import load
from app.grouping import boucher
from app.file import xlsx
from app.data.formatter import ReportFormatter


@click.command("group")
@click.argument('surveyfile', type=click.Path(exists=True), default='dataset.csv')
@click.option('-o', '--outputfile', show_default=True, default="output.csv", help="Enter the path to the output file.")
@click.option('-c', '--configfile', show_default=True, default="config.json", help="Enter the path to the config file.", type=click.Path(exists=True))
@click.option('--verify/--no-verify', show_default=True, default=False, help="Use this option to add verification reporting to the data.")
@click.option('-r', '--reportfile', show_default=True, help="report filename, relies on --verify flag being enabled")
def group(surveyfile: str, outputfile: str, configfile: str, verify: bool, reportfile: str):
    '''Group Users - forms groups for the users from the survey.

    SURVEYFILE is path to the raw survey output. [default=dataset.csv]
    '''

    config_data: models.Configuration = config.read_json(configfile)

    reader: load.SurveyDataReader = load.SurveyDataReader(
        config_data['field_mappings'])

    data: list[models.SurveyRecord] = reader.load(surveyfile)
    # Perform pre-grouping error checking
    if core.pre_group_error_checking(config_data["target_group_size"], data):
        return  # error found -- don't continue

    # Determine number of groups
    num_groups: int = core.get_num_groups(
        data, config_data["target_group_size"])

    if num_groups < 0:
        click.echo('''
                   **********************
                   Error: Not possible to adhere to the target_group_size (+/- 1) defined in the config file (config.json) in use.
                   **********************
                   ''')
        return

    # Create random groupings
    groups: list[models.GroupRecord]
    groups = boucher.create_groups(config_data, data)
        
    # For now, simply print the groups to the terminal (until file output is implemented)
    for grouping in groups:
        print(f'***** Group #{grouping.group_id} *****')
        for student in grouping.members:
            click.echo(student.student_id)
    click.echo("**********************")
    click.echo(outputfile)

    output.WriteGroupingData(config_data).output_groups_csv(groups, outputfile)

    if verify:
        report_filename = f'{outputfile.removesuffix(".csv")}_report.xlsx'
        if reportfile:
            report_filename = reportfile
        click.echo(f'Writing report to: "{report_filename}"')
        write_report(
            groups, config_data, report_filename)


def write_report(groups: list[models.GroupRecord], data_config: models.Configuration, filename: str):
    '''
    writes the report to an xlsx file
    '''
    formatter = ReportFormatter(data_config)
    formatted_data = formatter.format_individual_report(groups)
    group_formatted_report = formatter.format_group_report(groups)
    overall_formatted_report = formatter.format_overall_report(groups)
    xlsx_writer = xlsx.XLSXWriter(filename)
    xlsx_writer.write_sheet('individual_report', formatted_data)
    xlsx_writer.write_sheet('group_report', group_formatted_report)
    xlsx_writer.write_sheet('overall_report', overall_formatted_report)
    xlsx_writer.save()
