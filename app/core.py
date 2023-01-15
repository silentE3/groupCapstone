"""
Core grouping class for general functionality
"""

import click
from app import models


def get_stand_num_groups(survey_data: list, target_group_size: int) -> int:
    '''
    Function for determining the "standard" number of groups that the students
        could be seperated into based upon the number of students and
        the target group size.
    Note: A target_group_size value <=0 will be set to 1.
    Returns -1 if it is not possible to adhere to the target group
        size +/-1 (e.g. target = 6 with 8 total students)
    '''
    # calculate the number of groups based on number of students and target group size
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


def get_min_max_num_groups(survey_data: list, target_group_size: int) -> list[int]:
    '''
    Function for determining the number of groups that the
        students can be seperated into based upon the number of students
        and the target group size/target group size + 1.
    Returns an empty list if it is not possible to adhere to the target group
        size/target group size + 1 (e.g. target = 6 with 8 total students)
    Returns [min, max] values otherwise
    '''
    # calculate the number of groups based on number of students and target group
    #  size/target group size + 1
    if target_group_size <= 0 or len(survey_data) < 1:
        # protection from invalid group size input and survey data input
        return []

    min_max_num_groups: list[int] = []
    # min possible number groups focusing on target group size + 1
    min_max_num_groups.append(-(-len(survey_data) // (target_group_size + 1)))
    # max possible number groups focusing on target group size
    # NOTE: When using target group size +/-1, need to clamp (target group size -1) to
    #  > 0 to avoid divide by zero
    min_max_num_groups.append(len(survey_data)//(target_group_size))

    # make sure it is possible to create [min, max] num of groups while
    # adhering to target group size / target group size + 1
    for num_groups in range(min_max_num_groups[0], min_max_num_groups[1] + 1):
        if not (((target_group_size) * num_groups <= len(survey_data)) and
                (((target_group_size + 1) * num_groups >= len(survey_data)))):
            return []  # not possible to adhere to target group size/target group size + 1
    # if minimum num groups > max num groups, then not possible
    if min_max_num_groups[0] > min_max_num_groups[1]:
        return []  # not possible to adhere to target group size/target group size + 1
    return min_max_num_groups


def pre_group_error_checking(target_group_size: int, surveys_list: list[models.SurveyRecord]) -> bool:
    '''
    Perform pre-grouping error checking:
    - Ensure target group size is valid
    - Ensure the number of student surveys is valid
    Returns True if error found, and False otherwise.
    '''
    # target_group_size error checking
    if target_group_size <= 0:
        click.echo('**********************')
        click.echo(
            f'Error: Invalid target_group_size of {str(target_group_size)} defined in the config file.')
        click.echo('**********************')
        return True
    if len(surveys_list) == 0:
        click.echo('''
**********************
Error: No student surveys found in the input datafile.
**********************
                ''')
        return True

    # make sure it is possible to adhere to the target group size/target group size + 1
    if not get_min_max_num_groups(surveys_list, target_group_size):
        click.echo('''
**********************
Error: Not possible to adhere to the target_group_size / target_group_size + 1 defined in the config file (config.json) in use.
**********************
                   ''')
        return True
    return False
