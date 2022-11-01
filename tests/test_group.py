from click.testing import CliRunner
import click
from app.commands import group

runner = CliRunner()

# These tests verify the functionality in grouping.py.
# HOWEVER, this is really just a placeholder at this time since this
#   functionality (grouping) hans't truly been implemented yet. Therefore, the
#   testing is by no means exhaustive at this time


def test_group_1():
    '''
    Test of grouping six students with a target group size of 2.
    '''

    response = runner.invoke(group.group, [
                             '--datafile', './tests/test_files/survey_results/Example_Survey_Results_2.csv', '--configfile', './tests/test_files/configs/config_1.json'])
    assert response.exit_code == 0

    # Verify that the proper number of groups were created
    expected_num_groups = 3
    for i in range(0, expected_num_groups):
        statement = "Group #" + str(i+1)
        assert statement in response.output

    # Verify that all students were assigned to a group
    expected_students = ['jsmith1', 'jdoe2',
                         'mmuster3', 'jschmo4', 'bwillia5', 'mmuster3']
    for student in expected_students:
        assert student in response.output


def test_group_bad_datafile():
    response = runner.invoke(group.group, [
                             '--datafile', './tests/test_files/test_bad_file'])
    assert response.exit_code == 2
    assert response.exception


def test_group_bad_configfile():
    response = runner.invoke(group.group, [
                             '--datafile', 'tests/test_files/survey_results/Example_Survey_Results_1.csv',
                             '--configfile', './tests/test_files/test_bad_file'
                             ])
    assert response.exit_code == 2
    assert response.exception
