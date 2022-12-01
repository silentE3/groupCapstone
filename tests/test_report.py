import os
from click.testing import CliRunner
import click
from app.commands import report
from tests.test_utils.helper_functions import verify_rand_groups
from os.path import exists

runner = CliRunner()

# These tests verify the functionality in report.py.

def test_dev_reporting_basic():
    '''
    Runs a simple test against the dev data set 
    '''
    response = runner.invoke(report.report, [
                             './tests/test_files/dev_data/output.csv', 
                             './tests/test_files/dev_data/dataset-dev.csv',
                             '-c', './tests/test_files/dev_data/config-dev.json'])
    assert response.exit_code == 0    

    assert exists("./grouping_results_report.xlsx")
      
    os.remove("./grouping_results_report.xlsx")

def test_dev_reporting_report_file_specified():
    '''
    Runs a simple test against the dev data set but
    specifies the report output file name
    '''
    response = runner.invoke(report.report, [
                             './tests/test_files/dev_data/output.csv', 
                             './tests/test_files/dev_data/dataset-dev.csv',
                             '-c', './tests/test_files/dev_data/config-dev.json',
                             '-r', './tests/test_files/dev_data/specific_report.xlsx'])
    assert response.exit_code == 0    

    assert exists("./tests/test_files/dev_data/specific_report.xlsx")
      
    os.remove("./tests/test_files/dev_data/specific_report.xlsx")    

def test_invalid_group_file():
    '''
    Runs a simple test to ensure it fails on a bad file
    '''
    response = runner.invoke(report.report, [
                             './tests/test_files/dev_data/badfile.csv', 
                             './tests/test_files/dev_data/dataset-dev.csv',
                             '-c', './tests/test_files/dev_data/config-dev.json',
                             '-r', './tests/test_files/dev_data/specific_report.xlsx'])
    assert response.exit_code == 2   

def test_invalid_survey_file():
    '''
    Runs a simple test to ensure it fails on a bad file
    '''
    response = runner.invoke(report.report, [
                             './tests/test_files/dev_data/output.csv', 
                             './tests/test_files/dev_data/badfile.csv',
                             '-c', './tests/test_files/dev_data/config-dev.json',
                             '-r', './tests/test_files/dev_data/specific_report.xlsx'])
    assert response.exit_code == 2   

def test_invalid_config_file():
    '''
    Runs a simple test to ensure it fails on a bad file
    '''
    response = runner.invoke(report.report, [
                             './tests/test_files/dev_data/output.csv', 
                             './tests/test_files/dev_data/dataset-dev.csv',
                             '-c', './tests/test_files/dev_data/badfile.json',
                             '-r', './tests/test_files/dev_data/specific_report.xlsx'])
    assert response.exit_code == 2   
