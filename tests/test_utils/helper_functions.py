'''
Contains helper functions for test scripts.
'''

from app.data import load
from app import config, models


def verify_groups(report_filename: str, expected_min_num_groups: int,
                  expected_max_num_groups: int, expected_students_asurite: list[str]):
    '''
    Helper function that verifies the following for a grouping solution:
    - The proper/expected number of groups were created
    - The expected students (and only thoses students) were grouped

    output_filename: str -- String contiaing csv filename for the grouping results.
    expected_num_groups: int -- The expected number of groups.
    expected_students: list[str] -- list containing the expected students' asurite.
    '''

    # Verify that:
    #   - all students were assigned to a group
    #   - only the expected students were assigned to a group and only once

    config_data: models.Configuration = config.read_report_config(
        report_filename)
    survey_data = load.read_report_survey_data(report_filename,
                                               config_data['field_mappings'])
    # returns a list of group record lists
    group_solutions: list[list[models.GroupRecord]] = load.read_report_groups(
        report_filename, survey_data.records)
    
    # Verify that the proper number of groups were created

    for groups in group_solutions:
        students = []
        # check that the groups are the expected size
        assert len(groups) >= expected_min_num_groups and len(
            groups) <= expected_max_num_groups
        # get all of the members from the groups
        for group in groups:
            for member in group.members:
                students.append(member.student_id)
        # Verify the expected number of students were in the groupings
        for asurite in expected_students_asurite:
            assert asurite in students

        assert len(students) == len(expected_students_asurite)


def verify_all_students(report_filename: str, expected_min_num_groups: int,
                  expected_max_num_groups: int, expected_students_asurite: list[str]):
    '''
    Helper function that verifies the following for a grouping solution:
    - The solution includes the expected number of students

    output_filename: str -- String contiaing csv filename for the grouping results.
    expected_num_groups: int -- The expected number of groups.
    expected_students: list[str] -- list containing the expected students' asurite.
    '''

    config_data: models.Configuration = config.read_report_config(
        report_filename)
    survey_data = load.read_report_survey_data(report_filename,
                                               config_data['field_mappings'])
    # returns a list of group record lists
    group_solutions: list[list[models.GroupRecord]] = load.read_report_groups(
        report_filename, survey_data.records)

    # Verify that the proper number of groups were created

    for groups in group_solutions:
        students = []
        # check that the groups are the expected size
        assert len(groups) >= expected_min_num_groups and len(
            groups) <= expected_max_num_groups
        # get all of the members from the groups
        for group in groups:
            for member in group.members:
                students.append(member.student_id)

        assert len(students) == len(expected_students_asurite)