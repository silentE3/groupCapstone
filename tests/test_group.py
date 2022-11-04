from click.testing import CliRunner
import click
from app.commands import group
from tests.test_utils.helper_functions import verify_rand_groups

runner = CliRunner()

# These tests verify the functionality in grouping.py.
# HOWEVER, this is really just a placeholder at this time since this
#   functionality (grouping) hans't truly been implemented yet. Therefore, the
#   testing is by no means exhaustive at this time


def test_group_1():
    '''
    Test of grouping six students with a target group size of 2 (divides evenly).
    '''

    response = runner.invoke(group.group, [
                             '--datafile', './tests/test_files/survey_results/Example_Survey_Results_2.csv', '--configfile', './tests/test_files/configs/config_1.json'])
    assert response.exit_code == 0

    expected_num_groups = 3
    expected_students = ['jsmith1', 'jdoe2',
                         'mmuster3', 'jschmo4', 'bwillia5', 'mbrown6']
    verify_rand_groups(response.output, expected_num_groups, expected_students)


def test_group_2():
    '''
    Test of grouping eight students with a target group size of 5 (does not divide evenly,
    but still possible to maintain +/- 1 with rounding UP to two groups).
    '''

    response = runner.invoke(group.group, [
                             '--datafile', './tests/test_files/survey_results/Example_Survey_Results_5.csv', '--configfile', './tests/test_files/configs/config_3.json'])
    assert response.exit_code == 0

    expected_num_groups = 2
    expected_students = ['adumble4', 'triddle8', 'dmalfoy7',
                         'rweasle3', 'hgrange2', 'rhagrid5', 'hpotter1', 'nlongbo6']
    verify_rand_groups(response.output, expected_num_groups, expected_students)


def test_group_3():
    '''
    Test of grouping eight students with a target group size of 7 (does not divide evenly,
    but still possible to maintain +/- 1 with rounding DOWN to one group).
    '''

    response = runner.invoke(group.group, [
                             '--datafile', './tests/test_files/survey_results/Example_Survey_Results_5.csv', '--configfile', './tests/test_files/configs/config_4.json'])
    assert response.exit_code == 0

    expected_num_groups = 1
    expected_students = ['adumble4', 'triddle8', 'dmalfoy7',
                         'rweasle3', 'hgrange2', 'rhagrid5', 'hpotter1', 'nlongbo6']
    verify_rand_groups(response.output, expected_num_groups, expected_students)


def test_group_size_not_possible():
    '''
    Test of grouping eight students with a target group size of 6 (does not divide evenly and
    NOT possible to maintain +/- 1 of target group size). Should return an error message.
    '''

    response = runner.invoke(group.group, [
                             '--datafile', './tests/test_files/survey_results/Example_Survey_Results_5.csv', '--configfile', './tests/test_files/configs/config_5.json'])
    assert response.exit_code == 0

    # Verify that no groups were created
    assert "Group #" not in response.output

    # Verify that an Error message is displayed to the user
    assert "Error:" in response.output


def test_group_invalid_group_size():

    response = runner.invoke(group.group, [
                             '--datafile', './tests/test_files/survey_results/Example_Survey_Results_5.csv', '--configfile', './tests/test_files/configs/config_6.json'])
    assert response.exit_code == 0

    # Verify that no groups were created
    assert "Group #" not in response.output

    # Verify that an Error message is displayed to the user
    assert "Error:" in response.output


def test_group_zero_surveys():

    response = runner.invoke(group.group, [
                             '--datafile', './tests/test_files/survey_results/Example_Survey_Results_6.csv', '--configfile', './tests/test_files/configs/config_5.json'])
    assert response.exit_code == 0

    # Verify that no groups were created
    assert "Group #" not in response.output

    # Verify that an Error message is displayed to the user
    assert "Error:" in response.output


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
