'''
Contains helper functions for test scripts.
'''

from app.data import load
from app import config, models


def verify_groups(report_filename: str, survey_filename: str, expected_min_num_groups: int,
                  expected_max_num_groups: int, expected_students_asurite: list[str]):
    '''
    Helper function that verifies the following for a grouping solution:
    - The proper/expected number of groups were created
    - The expected students (and only thoses students) were grouped

    output_filename: str -- String contiaing csv filename for the grouping results.
    expected_num_groups: int -- The expected number of groups.
    expected_students: list[str] -- list containing the expected students' asurite.
    '''

    # file = open(report_filename, "r", encoding="utf-8-sig")
    # content = file.readlines()
    # file.close()

    # Verify that:
    #   - all students were assigned to a group
    #   - only the expected students were assigned to a group and only once

    config_data: models.Configuration = config.read_report_config(report_filename)
    survey_data = load.read_report_survey_data(report_filename,
                                               config_data['field_mappings'])
    groups: list[list[models.GroupRecord]] = load.read_report_groups(report_filename, survey_data.records)
    # Verify that the proper number of groups were created
    assert len(groups) >= expected_min_num_groups and len(
        groups) <= expected_max_num_groups
    students = []

    for group in groups:
        # first item is group, second item is student
        for gr in group:
            for asurite in expected_students_asurite:
                student = load.__get_user_by_id(asurite, gr.members)
                print(student)
                assert student
                assert student not in students
                students.append(student)
    # Verify the expected number of students were in the groupings
    assert len(students) == len(expected_students_asurite)

