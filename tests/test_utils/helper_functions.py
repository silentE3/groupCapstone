'''
Contains helper functions for test scripts.
'''


def verify_rand_groups(output: str, expected_num_groups: int, expected_students: list[str]):
    '''
    Helper function that verifies the following for the random student grouping:
    - The proper/expected number of groups were created
    - The expected students (and only thoses students) were grouped

    output: str -- String that is output to the terminal describing the groups formed.
    expected_num_groups: int -- The expected number of groups.
    expected_students: list[str] -- list containing the expected students' asurite.
    '''

    # Verify that all students were assigned to a group
    for student in expected_students:
        assert student in output

    output_lines: list[str]
    output_lines = output.split('\n')  # individual lines of output
    # Verify that ONLY the expected students were assigned to a group and only once
    student_count = 0
    group_count = 0
    while len(output_lines) >= 1 and not ((output_lines[0]).__contains__("Group #")):
        # get rid of any lines prior to the start of the grouping
        output_lines.pop(0)
    for line in output_lines:
        if line.__contains__("Group #"):
            group_count += 1
        elif line.__contains__("**********************"):
            break
        else:
            assert expected_students.__contains__(line)
            student_count += 1
    assert student_count == len(expected_students)

    # Verify that the proper number of groups were created
    assert group_count == expected_num_groups
    for i in range(0, expected_num_groups):
        statement = "Group #" + str(i+1)
        assert statement in output
    statement = "Group #" + str(expected_num_groups + 1)
    assert statement not in output  # no "extra" groups

    # Verify "Error:" is NOT included in the output
    assert "Error:" not in output
