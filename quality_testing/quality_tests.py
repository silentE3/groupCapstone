import os
from click.testing import CliRunner
import math
from app.commands import group
from tests.test_utils.helper_functions import verify_groups
from tests.test_utils.helper_functions import verify_all_students

runner = CliRunner()

'''
These tests were created for the quality plan created for the project.  They will not run every time there is a pull 
request.  Some of the quality tests were alredy part of our testing regime, and those will remain in the tests package.
'''

def test_complete_solution():
    '''
    This test is to verify that when a surveyfile containing 100 students is provided to the program, with a target
    group size of 5 with a tolarance of +1, the program will produce a grouping solution with all 100 students grouped
    '''
    complete_solution = runner.invoke(group.group, ['./tests/test_files/survey_results/Example_Survey_Results_100.csv',
                                                   '-c', './tests/test_files/configs/config_100.json'])
    expected_min_num_groups = 17
    expected_max_num_groups = 20
    expected_students = [(lambda x: f"asurite{x}")(x) for x in range(1, 101)]

    assert complete_solution.exit_code == 0

    verify_all_students('./tests/test_files/survey_results/Example_Survey_Results_100_report.xlsx', expected_min_num_groups,
                  expected_max_num_groups, expected_students)

    os.remove('./tests/test_files/survey_results/Example_Survey_Results_100_report.xlsx')

def test_group_quality_2():
    '''
    Test of grouping 16 students with a target group size of 3 (does not divide evenly,
    but still possible to maintain +1, [group sizes of 3 or 4]).
    '''

    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_16.csv', '--configfile', './tests/test_files/configs/config_16.json', '--reportfile', './tests/test_files/survey_results/test_16_report.xlsx'])
    assert response.exit_code == 0

    expected_students = ['adumble4', 'triddle8', 'dmalfoy7',
                         'rweasle3', 'hgrange2', 'rhagrid5', 'hpotter1', 'nlongbo6',
                         'adumble4_2', 'triddle8_2', 'dmalfoy7_2',
                         'rweasle3_2', 'hgrange2_2', 'rhagrid5_2', 'hpotter1_2', 'nlongbo6_2']
    verify_groups('./tests/test_files/survey_results/test_16_report.xlsx', 4,
                  5, expected_students)
    # Verify "Error:" is NOT included in the output
    assert "Error:" not in response.output

    os.remove('./tests/test_files/survey_results/test_16_report.xlsx')

def test_group_quality_3():
    '''
    Test of grouping 19 students with a target group size of 5 and a tolerance of -1.
    [group sizes of 4 or 5]
    '''
    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_19.csv', '--configfile', './tests/test_files/configs/config_19.json', '--reportfile', './tests/test_files/survey_results/test_19_report.xlsx'])
    assert response.exit_code == 0

    expected_students = ['uenterprise2', 'uhornet3', 'uyorktown1',
                         'ulexington4', 'usaratoga5', 'jakagi6',
                         'jkaga7', 'jzuikaku8', 'jshokaku9',
                         'uenterprise2_2', 'uhornet3_2', 'uyorktown1_2',
                         'ulexington4_2', 'usaratoga5_2', 'jakagi6_2',
                         'jkaga7_2', 'jzuikaku8_2', 'jshokaku9_2', 'jhiryu10']
    verify_groups('./tests/test_files/survey_results/test_19_report.xlsx', 3,
                  4, expected_students)
    # Verify "Error:" is NOT included in the output
    assert "Error:" not in response.output

    os.remove('./tests/test_files/survey_results/test_19_report.xlsx')

def test_group_quality_5():
    '''
    Test of grouping 10 students with a target group size of 7 and a tolerance of +/-.
    This should end in error.
    '''
    response = runner.invoke(group.group, [
                             './tests/test_files/survey_results/Example_Survey_Results_10.csv', '--configfile', './tests/test_files/configs/config_10.json', '--reportfile', './tests/test_files/survey_results/test_10_report.xlsx'])
    assert response.exit_code == 0

    expected_students = ['uenterprise2', 'uhornet3', 'uyorktown1',
                         'ulexington4', 'usaratoga5', 'jakagi6',
                         'jkaga7', 'jzuikaku8', 'jshokaku9', 'jhiryu10']
    verify_groups('./tests/test_files/survey_results/test_19_report.xlsx', 3,
                  4, expected_students)
    # Verify "Error:" is NOT included in the output
    assert "Error:" in response.output

    os.remove('./tests/test_files/survey_results/test_19_report.xlsx')