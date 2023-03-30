import os
from click.testing import CliRunner
import math
from app.commands import group
from tests.test_utils.helper_functions import verify_groups


runner = CliRunner()

# These tests verify the functionality in group.py.
# HOWEVER, this is really just a placeholder at this time since this
#   functionality (grouping) hans't truly been implemented yet. Therefore, the
#   testing is by no means exhaustive at this time


def test_group_1():
    '''
    Test of grouping 12 students with a target group size of 4 (divides evenly), without any +/- margin. 

    T-01
    '''

    response = runner.invoke(group.group, [
        './tests/test_files/survey_results/test_group_1.csv', '--configfile', './tests/test_files/configs/test_group_1_config.json'])
    assert response.exit_code == 0

    expected_min_num_groups = 3
    expected_max_num_groups = 3
    expected_students = ['jsmith1', 'jdoe2',
                         'mmuster3', 'jschmo4', 'bwillia5', 'mbrown6', 'charles7', 'carl8', 'elee9', 'cred10', 'bobbylee11', 'jrogan12']

    verify_groups('./tests/test_files/survey_results/test_group_1_report.xlsx', expected_min_num_groups,
                  expected_max_num_groups, expected_students)

    # Verify "Error:" is NOT included in the output
    assert "Error:" not in response.output

    os.remove(
        './tests/test_files/survey_results/test_group_1_report.xlsx')


def test_group_2():
    '''
    Test of grouping 8 students with a target group size of 5 (does not divide evenly,
    but still possible to maintain +/- 1 with rounding UP to two groups).
    '''

    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_5.csv', '--configfile', './tests/test_files/configs/config_3.json'])
    assert response.exit_code == 0

    expected_min_num_groups = math.ceil(8/(5+1))
    expected_max_num_groups = 8//(5-1)
    expected_students = ['adumble4', 'triddle8', 'dmalfoy7',
                         'rweasle3', 'hgrange2', 'rhagrid5', 'hpotter1', 'nlongbo6']
    verify_groups("./tests/test_files/survey_results/Example_Survey_Results_5_report.xlsx", expected_min_num_groups,
                  expected_max_num_groups, expected_students)
    # Verify "Error:" is NOT included in the output
    assert "Error:" not in response.output

    os.remove(
        './tests/test_files/survey_results/Example_Survey_Results_5_report.xlsx')


def test_group_3():
    '''
    Test of grouping 8 students with a target group size of 7 (does not divide evenly,
    but still possible to maintain +/- 1 with rounding DOWN to one group).
    '''

    expected_min_num_groups = math.ceil(8/(7+1))
    expected_max_num_groups = 8//(7-1)
    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_5.csv', '--configfile', './tests/test_files/configs/config_4.json', '--reportfile', './tests/test_files/survey_results/test_3_report.xlsx'])
    assert response.exit_code == 0

    expected_num_groups = 1
    expected_students = ['adumble4', 'triddle8', 'dmalfoy7',
                         'rweasle3', 'hgrange2', 'rhagrid5', 'hpotter1', 'nlongbo6']
    verify_groups('./tests/test_files/survey_results/test_3_report.xlsx', expected_min_num_groups,
                  expected_max_num_groups, expected_students)
    # Verify "Error:" is NOT included in the output
    assert "Error:" not in response.output

    os.remove('./tests/test_files/survey_results/test_3_report.xlsx')

def test_group_size_not_possible():
    '''
    Test of grouping eight students with a target group size of 6 (does not divide evenly and
    NOT possible to maintain +/- 1 of target group size). Should return an error message.
    '''

    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_5.csv', '--configfile', './tests/test_files/configs/config_5.json'])
    assert response.exit_code == 0

    # Verify that no groups were created
    assert "Group #" not in response.output

    # Verify that an Error message is displayed to the user
    assert "Error:" in response.output


def test_group_invalid_group_size():

    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_5.csv', '--configfile', './tests/test_files/configs/config_5.json', '--reportfile', './tests/test_files/survey_results/report_bad_group_size.xlsx'])
    assert response.exit_code == 0

    # Verify that no groups were created
    assert "Group #" not in response.output

    # Verify that an Error message is displayed to the user
    assert "Error:" in response.output


def test_group_zero_surveys():

    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_6.csv', '--configfile', './tests/test_files/configs/config_5.json'])
    assert response.exit_code == 0

    # Verify that no groups were created
    assert "Group #" not in response.output

    # Verify that an Error message is displayed to the user
    assert "Error:" in response.output


def test_group_bad_datafile():
    '''
    Test bad data file
    '''
    response = runner.invoke(group.group, [
                             './tests/test_files/test_bad_file'])
    assert response.exit_code == 2
    assert response.exception


def test_group_bad_configfile():
    '''
    Test bag config
    '''
    response = runner.invoke(group.group, [
                             'tests/test_files/survey_results/Example_Survey_Results_1.csv',
                             '--configfile', './tests/test_files/test_bad_file'
                             ])
    assert response.exit_code == 2
    assert response.exception


def test_group_verify_and_report_file_name_1():
    '''
    Test of grouping six students with a target group size of 2 (divides evenly).
    '''

    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_2.csv', '--configfile', './tests/test_files/configs/config_1.json', '--reportfile', 'test_verify_and_report_file_name_1_report.xlsx'])
    assert response.exit_code == 0

    assert response.output.endswith(
        'Writing report to: test_verify_and_report_file_name_1_report.xlsx\n')
    os.remove('test_verify_and_report_file_name_1_report.xlsx')


def test_alt_command_args_1():
    '''
    Should be same as test_group_verify_and_report_file_name_1 but using the altername command line args
    '''

    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_2.csv', '-c', './tests/test_files/configs/config_1.json', '-r', 'test_verify_and_report_file_name_1_report.xlsx'])
    assert response.exit_code == 0

    assert response.output.endswith(
        'Writing report to: test_verify_and_report_file_name_1_report.xlsx\n')
    os.remove('test_verify_and_report_file_name_1_report.xlsx')
