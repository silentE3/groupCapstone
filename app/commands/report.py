'''
verify contains all the commands for verifying the results
of a grouping
'''

import click
from app import config, models
from app.data import load, reporter


@click.command("update-report")
@click.argument('reportfile', type=click.Path(exists=True), default="group_report.xlsx")
def update_report(reportfile: str):
    '''
    update-report - reads in a previously generated report and updates it based on changes made to it

    REPORTFILE is the path to the xlsx based report file to read in
    '''

    config_data: models.Configuration = config.read_report_config(reportfile)

    # load the survey data
    survey_data = load.read_report_survey_data(reportfile,
                                               config_data['field_mappings'])

    groups: list[list[models.GroupRecord]] = load.read_report_groups(
        reportfile, survey_data.records)

    click.echo(f'Writing updated report to: "{reportfile}"')
    reporter.write_report(groups, survey_data,
                          config_data, reportfile)
 # Delete if no problems
 # ~~~~~~~~~~~~~~~~~~~~~~survey_data.raw_rows~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~