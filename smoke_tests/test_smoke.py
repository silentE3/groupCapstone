'''
Smoke tests
'''


import os
from tests.test_group import test_group_2, test_group_bad_datafile, test_group_invalid_group_size
from tests.test_guide import test_group_command, test_guide_lists_commands, test_update_report_command, test_create_report_command
from tests.test_report import test_dev_reporting_basic, test_invalid_group_file, test_update_report_basic, test_update_report_invalid_report_file
from click.testing import CliRunner
from app.commands import cli


runner = CliRunner()


def test_smoke_test():
    '''
    Manual run smoke tests 
    '''
    test_guide_lists_commands()
    test_group_command()
    test_update_report_command()
    test_create_report_command()
    test_dev_reporting_basic()
    test_invalid_group_file()
    test_update_report_basic()
    test_update_report_invalid_report_file()
    test_group_bad_datafile()
    test_group_2()
    test_group_invalid_group_size()

    response = runner.invoke(cli.generate.gen)
    assert "Created new survey dataset: \"dataset.csv\"" in response.output
    # os.remove('./dataset.csv') #keep this file. It already exists

    response = runner.invoke(cli.report.update_report)
    assert "Error: Invalid value for '[REPORTFILE]': Path 'group_report.xlsx' does not exist." in response.output
      
    response = runner.invoke(cli.report.report)
    assert "Error: Invalid value for '[GROUPFILE]': Path 'output.csv' does not exist." in response.output
  
