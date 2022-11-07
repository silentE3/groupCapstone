'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''


import os
import click

from app import config, core, output
from app import models
from app.data import load
from app.grouping.randomizer import RandomGrouper


@click.command("group")
@click.option('-d', '--datafile', show_default=True, default="dataset.csv", help="Enter the path to the data file.")
@click.option('-o', '--outputfile', show_default=True, default="output.csv", help="Enter the path to the output file.")
@click.option('-c', '--configfile', show_default=True, default="config.json", help="Enter the path to the config file.")
@click.option('--v', is_flag=True, show_default=True, default=False, help="Perform veryification of group data and output tally.")
@click.option('-r', '--groupreport', show_default=True, default="", help="Enter the path to the group report output file.")
# pylint: disable=duplicate-code
def group(datafile: str, outputfile: str, configfile: str, v: bool, groupreport: str): # pylint: disable=invalid-name
    '''
    runs the grouping functionality
    '''

    if not os.path.exists(datafile):
        raise click.BadOptionUsage('--datafile',
                                   f'no datafile found in the given path: "{datafile}"')

    if not os.path.exists(configfile):
        raise click.BadOptionUsage(
            '--configfile', f'no config file found in the given path "{configfile}"')

    config_data: models.Configuration = config.read_json(configfile)
    reader: load.SurveyDataReader = load.SurveyDataReader(
        config_data['field_mappings'])
    data: list[models.SurveyRecord] = reader.load(datafile)

    # Perform pre-grouping error checking
    target_group_size: int = config_data["target_group_size"]
    if core.pre_group_error_checking(target_group_size, data):
        return  # error found -- don't continue

    # Determine number of groups
    num_groups: int
    num_groups = core.get_num_groups(data, config_data["target_group_size"])

    if num_groups < 0:
        print("\n**********************")
        print("Error: Not possible to adhere to the target_group_size of " + str(target_group_size) +
              " (+/- 1) defined in the config file.")
        print("**********************\n")
        return

    # Create random groupings
    groups: list[models.GroupRecord]
    grouper = RandomGrouper()
    groups = grouper.create_groups(
        data, config_data["target_group_size"], num_groups)

    # For now, simply print the groups to the terminal (until file output is implemented)
    for grouping in groups:
        print("***** " + grouping.group_id + " *****")
        for student in grouping.members:
            print(student.student_id)
    print("**********************")

    print(outputfile)

    group_csv_writer = output.WriteGroupingData(config_data)
    group_csv_writer.output_groups_csv(groups, outputfile)

    if v:
        if len(groupreport) == 0:
            # for now we are just assuming the .csv is lowercase
            groupreport = outputfile.removesuffix(".csv") + "_report.xslx"

        print(f'Will verify and output report to "{groupreport}"')
        