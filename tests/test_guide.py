import os
import shutil
from click.testing import CliRunner
from unittest.mock import patch
from app.commands import cli

runner = CliRunner()

'''
These test are to verify the proper functioning of the guided UI.  They will mock user input to verify that the input is
also being handled correctly
'''

def test_guide_lists_commands():
    result = runner.invoke(cli.guide, input='quit\n')
    assert 'Available commands:' in result.output
    assert 'group' in result.output
    assert 'update report' in result.output
    assert 'create report' in result.output


@patch('app.commands.group.group')
def test_group_command(mock_group):
    result = runner.invoke(cli.guide, input='group\ntests/test_files/dev_data/dataset-dev.csv\n'
                                        'tests/test_files/dev_data/config-dev.json\nN\nN\n')
    assert 'Enter the path to the survey file' in result.output
    assert 'Enter the path to the config file' in result.output
    assert not 'Enter the path to the existing report file' in result.output
    assert not 'Enter the path to the file containing all student IDs' in result.output
    assert mock_group.called_with('tests/test_files/dev_data/dataset-dev.csv', 'tests/test_files/dev_data/config-dev.json', None, None)

@patch('app.commands.report.update_report')
def test_update_report_command(mock_update_report):
    report_file_path: str = 'tests/test_files/reports/Example_Report_1'
    shutil.copyfile(report_file_path + '.xlsx',
                    report_file_path + '_copy.xlsx')

    original_file_time: float = os.path.getmtime(report_file_path + '.xlsx')
    result = runner.invoke(cli.guide, input='update report\n' + report_file_path + '_copy.xlsx\n')
    assert 'Enter the path to the existing report file' in result.output
    assert mock_update_report.called_with('dataset_report.xlsx')

    # check file was updated
    assert os.path.getmtime(report_file_path + '_copy.xlsx') > original_file_time

    os.remove(report_file_path + '_copy.xlsx')

@patch('app.commands.report.report')
def test_create_report_command(mock_report):
    result = runner.invoke(cli.guide, input='create report\ntests/test_files/dev_data/output.csv\n'
                                            'tests/test_files/dev_data/dataset-dev.csv\n'
                                            'tests/test_files/dev_data/config-dev.json\nN\n')
    assert 'Enter the path to the grouping file' in result.output
    assert 'Enter the path to the raw survey file' in result.output
    assert 'Enter the path to the config file' in result.output
    assert not 'Enter the path to the existing report file' in result.output
    assert mock_report.called_with('output.csv', 'dataset.csv', None, 'config.json')
    os.remove('tests_report.xlsx')
