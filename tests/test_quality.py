import math
import os
from click.testing import CliRunner

from app.commands import group
from tests.test_utils.helper_functions import verify_groups

runner = CliRunner()


def test_valid_group_sizing_1():
    '''
    Test of grouping 12 students with a target group size of 4 with no tolerance.
    '''

    response = runner.invoke(group.group, [
        './tests/test_files/survey_results/Example_Survey_Results_2.csv', '--configfile', './tests/test_files/configs/config_1.json'])
    assert response.exit_code == 0

    expected_min_num_groups = math.ceil(6/(2+1))
    expected_max_num_groups = 6//(2-1)
    expected_students = ['jsmith1', 'jdoe2',
                         'mmuster3', 'jschmo4', 'bwillia5', 'mbrown6']

    verify_groups('./tests/test_files/survey_results/Example_Survey_Results_2_report.xlsx', expected_min_num_groups,
                  expected_max_num_groups, expected_students)

    # Verify "Error:" is NOT included in the output
    assert "Error:" not in response.output

    os.remove(
        './tests/test_files/survey_results/Example_Survey_Results_2_report.xlsx')