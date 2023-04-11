"""
Core grouping class for general functionality
"""

import click
from app import models


def get_num_groups(survey_data: list, target_group_size_in: int, target_plus_one_allowed: bool, target_minus_one_allowed: bool) -> int:
    '''
    Function for determining the number of groups that the students
        will be seperated into when adhering to the target group size
        to the extent possible.

    Returns -1 if it is not possible to adhere to the target group size +/- the
         configurable margins (e.g. target = 6 with a +/-1 margin and 8 total students)
    '''
    target_group_size: int = target_group_size_in

    # protection from invalid group size input
    if len(survey_data) == 0:
        return 0
    if target_group_size <= 0:
        if target_plus_one_allowed and (target_group_size + 1) > 0:
            target_group_size = 1
        else:
            return -1

    # Calculate the number of groups that best adheres to target group
    # size, while considering the configured margins
    num_groups: int = 0
    if ((target_minus_one_allowed and target_plus_one_allowed) or
            (not target_minus_one_allowed and not target_plus_one_allowed)):
        # standard rounding
        num_groups = round(len(survey_data) / target_group_size)
    elif target_minus_one_allowed:
        num_groups = -(-len(survey_data) // target_group_size)  # round down
    else:
        num_groups = len(survey_data) // target_group_size  # round up
    num_groups = max(num_groups, 1)  # make sure at least one group

    # make sure it is possible to adhere to the target group size +/- 1
    max_group_size: int = target_group_size_in + \
        1 if target_plus_one_allowed else target_group_size_in
    min_group_size: int = target_group_size_in - \
        1 if target_minus_one_allowed else target_group_size_in
    if not ((min_group_size * num_groups <= len(survey_data)) and
            ((max_group_size * num_groups >= len(survey_data)))):
        return -1  # not possible to adhere to the target group size +/- the configured margins

    return num_groups


def get_min_max_num_groups(survey_data: list, target_group_size: int, target_plus_one_allowed: bool, target_minus_one_allowed: bool) -> list[int]:
    '''
    Function for determining the number of groups that the
        students can be seperated into based upon the number of students
        and the target group size (+1 and/or -1, as applicable).
    Returns an empty list if it is not possible to adhere to the target group
        size and the allowed margin (e.g. target = 6 with a +/-1 margin and 8 total students)
    Returns [min, max] values otherwise
    '''
    # calculate the number of groups based on number of students and target group size +/- the
    #  allowable margin

    if target_group_size <= 0 or len(survey_data) < 1:
        # protection from invalid group size input and survey data input
        return []

    min_max_num_groups: list[int] = []

    # min possible number groups focusing on max allowable group size
    max_group_size: int = target_group_size + \
        1 if target_plus_one_allowed else target_group_size
    min_max_num_groups.append(-(-len(survey_data) // (max_group_size)))

    # max possible number groups focusing on min allowable group size
    min_group_size: int = target_group_size
    if target_minus_one_allowed and (target_group_size - 1) > 0:
        min_group_size -= 1
    min_max_num_groups.append(len(survey_data)//(min_group_size))

    # make sure it is possible to create [min, max] num of groups while
    # adhering to target group size and the allowable margin
    for num_groups in range(min_max_num_groups[0], min_max_num_groups[1] + 1):
        if not ((min_group_size * num_groups <= len(survey_data)) and
                (max_group_size * num_groups >= len(survey_data))):
            return []  # not possible to adhere to target group size and the allowable margin
    # if minimum num groups > max num groups, then not possible
    if min_max_num_groups[0] > min_max_num_groups[1]:
        return []  # not possible to adhere to target group size and the allowable margin

    return min_max_num_groups


def pre_group_error_checking(target_group_size: int, target_plus_one_allowed: bool,
                             target_minus_one_allowed: bool, surveys_list: list[models.SurveyRecord]) -> bool:
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

    # make sure it is possible to adhere to the target group size and the allowable margin
    if not get_min_max_num_groups(surveys_list, target_group_size, target_plus_one_allowed, target_minus_one_allowed):
        click.echo('''
**********************
Error: Not possible to adhere to the target_group_size and the allowable margin defined in the config file (config.json) in use.
**********************
                   ''')
        return True
    return False
