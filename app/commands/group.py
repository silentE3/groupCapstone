'''
group contains all the commands for reading in the .csv data files and generating groups.
Also includes reading in the configuration file.
'''

import random
import os
import click
from app import config, load
from app import models


@click.command("group")
@click.option('-d', '--datafile', default="dataset.csv", help="Enter the path to the data file.")
@click.option('-o', '--outputfile', default="output.csv", help="Enter the path to the output file.")
@click.option('-c', '--configfile', default="config.json", help="Enter the path to the config file.")
@click.option('--v', is_flag=True, default=False, help="Perform veryification of group data and output tally.")
@click.option('-t', '--tallyfile',  default="grouptally.csv", help="Enter the path to the group tally output file.")
# pylint: disable=duplicate-code
def group(datafile: str, outputfile: str, configfile: str, v: bool, tallyfile: str):  # pylint: disable=invalid-name
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
    if pre_group_error_checking(target_group_size, data):
        return  # error found -- don't continue

    # Determine number of groups
    num_groups: int
    num_groups = get_num_groups(data, target_group_size)

    if num_groups < 0:
        print("\n**********************")
        print("Error: Not possible to adhere to the target_group_size of " + str(target_group_size) +
              " (+/- 1) defined in the config file.")
        print("**********************\n")
        return

    # Create random groupings
    groups: list[list[models.SurveyRecord]]
    groups = create_random_groups(
        data, target_group_size, num_groups)

    # For now, simply print the groups to the terminal (until file output is implemented)
    for idx, grouping in enumerate(groups):
        print("***** Group #" + str(idx + 1) + " *****")
        for student in grouping:
            print(student.student_id)
    print("**********************")

    print(outputfile)

    if v:
        print(f'Will verify and output tally to "{tallyfile}"')


def pre_group_error_checking(target_group_size: int, surveys_list: list[models.SurveyRecord]) -> bool:
    '''
    Perform pre-grouping error checking:
    - Ensure target group size is valid
    - Ensure the number of student surveys is valid
    Returns True if error found, and False otherwise.
    '''
    # target_group_size error checking
    if target_group_size <= 0:
        print("\n**********************")
        print("Error: Invalid target_group_size of " + str(target_group_size) +
              " defined in the config file.")
        print("**********************\n")
        return True
    if len(surveys_list) == 0:
        print("\n**********************")
        print("Error: No student surveys found in the input datafile.")
        print("**********************\n")
        return True
    return False


def get_num_groups(survey_data: list, target_group_size: int) -> int:
    '''
    Function for determining the number of groups that the students
        will be seperated into based upon the number of students and
        the target group size.
    Returns -1 if it is not possible to adhere to the target group
        size +/-1 (e.g. target = 6 with 8 total students)
    '''
    # calculate the number of groups based on number of students & target group size
    if target_group_size <= 0:
        # protection from invalid group size input
        target_group_size = 1
    num_groups = round(len(survey_data) / target_group_size)
    num_groups = max(num_groups, 1)  # make sure at least one group

    # make sure it is possible to adhere to the target group size +/- 1
    if not (((target_group_size - 1) * num_groups <= len(survey_data)) and
            (((target_group_size + 1) * num_groups >= len(survey_data)))):
        return -1  # not possible to adhere to the target group size +/- 1

    return num_groups


def create_random_groups(survey_data: list,
                         target_group_size: int,
                         num_groups: int) -> list[list[models.SurveyRecord]]:
    '''
    function for grouping students randomly
    '''
    # Randomly shuffle the data in preparation for random grouping
    random.shuffle(survey_data)

    # Determine if non-target groups are larger or smaller (or if N/A)
    # (0 = all standard, 1 = some larger, -1 = some smaller)
    non_stand_mod = 0
    if (num_groups * target_group_size) < len(survey_data):
        non_stand_mod = 1
    elif (num_groups * target_group_size) > len(survey_data):
        non_stand_mod = -1

    # Determine number of groups with non-target size
    num_non_targ_groups = 0
    if non_stand_mod == 1:
        num_non_targ_groups = len(survey_data) % target_group_size
    if non_stand_mod == -1:
        num_non_targ_groups = target_group_size - \
            (len(survey_data) % target_group_size)

    result: list[list[models.SurveyRecord]]
    result = []
    survey_num = 0  # counter for which student we're assigning currently
    for i in range(0, num_groups):
        result.append([])  # create the group
        group_size = target_group_size
        if i >= (num_groups - num_non_targ_groups):
            # Groups with non-target size
            group_size += non_stand_mod
        for _ in range(0, group_size):
            result[i].append(survey_data[survey_num])
            survey_num += 1
    return result
