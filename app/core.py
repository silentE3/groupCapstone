"""
Core grouping class for general functionality
"""


from app import models


def get_num_groups(survey_data: list, target_group_size: int) -> int:
    '''
    Function for determining the number of groups that the students
        will be seperated into based upon the number of students and
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