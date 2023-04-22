'''
This quality test (refer to the project's Quality Plan) is a stress test that takes
a long time to execute. Therefore, it seemed best to separate it from the other quality
tests so that the others could be executed quickly without this one test significantly
prolonging the overall runtime.
'''

import math
import os
import time
from click.testing import CliRunner
from app.commands import group


runner = CliRunner()


def test_group_stress_t08():
    '''
    This test verifies that the tool is capable of grouping an extreme number of
    students (300) in an amount of time that has been defined as reasonable (8 hours),
    as specified by the associated metric (M4) and high-level requirement (4).
    '''

    TIME_LIMIT_MS: int = 28800000  # 8 hours as milliseconds
    NS_TO_MS_DIVISOR: int = 1000000

    start_time_ms: int = math.ceil(time.time_ns() / NS_TO_MS_DIVISOR)
    response = runner.invoke(group.group, ['tests/test_files/survey_results/dataset-300_students.csv',
                                           '--configfile', 'tests/test_files/configs/config-300_students.json'], pty=True)
    execution_time_ms: int = math.ceil(time.time_ns() / NS_TO_MS_DIVISOR) - start_time_ms
    print('\nExecution time (ms): ' + str(execution_time_ms) + '\n')
    assert execution_time_ms < TIME_LIMIT_MS
    assert response.exit_code == 0
    assert os.path.exists('tests/test_files/survey_results/dataset-300_students_report.xlsx')
    os.remove('tests/test_files/survey_results/dataset-300_students_report.xlsx')


# run the quality tests
tests = [test_group_stress_t08]
for test in tests:
    try:
        test()
    except AssertionError:
        print("FAIL  --  " + test.__name__)
    else:
        print("PASS  --  " + test.__name__)
