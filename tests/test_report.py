import os
import shutil
from click.testing import CliRunner
import click
from app.commands import report
from os.path import exists
from openpyxl import load_workbook, workbook

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


def test_update_report_basic():
    '''
    Runs a simple "update report" test against Example_Report_1.xlsx.
    '''

    report_file_path: str = './tests/test_files/reports/Example_Report_1'
    shutil.copyfile(report_file_path + '.xlsx',
                    report_file_path + '_copy.xlsx')

    original_file_time: float = os.path.getmtime(report_file_path + '.xlsx')

    response = runner.invoke(report.update_report, [
                             './tests/test_files/reports/Example_Report_1.xlsx'])
    assert response.exit_code == 0

    # verify the report file was updated
    assert os.path.getmtime(report_file_path + '.xlsx') > original_file_time

    os.remove(report_file_path + '.xlsx')
    os.rename(report_file_path + '_copy.xlsx', report_file_path + '.xlsx')


def test_update_report_invalid_report_file():
    '''
    Runs a simple test to ensure update-report fails on a bad report file
    '''
    response = runner.invoke(report.update_report, [
                             './tests/test_files/reports/Nonexistent_File.xlsx'])
    assert response.exit_code == 2

def test_dev_reporting_contains_sheets():
    '''
    Checks the generated excel file for the expected sheets
    For now, just config
    '''
    response = runner.invoke(report.report, [
                             './tests/test_files/dev_data/output.csv',
                             './tests/test_files/dev_data/dataset-dev.csv',
                             '-c', './tests/test_files/dev_data/config-dev.json'])
    assert response.exit_code == 0

    assert exists("./grouping_results_report.xlsx")

    book: workbook.Workbook = load_workbook("./grouping_results_report.xlsx")
    assert 'config' in list(book.sheetnames)
    # add more asserts for more sheet names here

    os.remove("./grouping_results_report.xlsx")

def test_colored_columns():
    '''
    Checks if the availability overlap column has a background color of Green.
    '''
    response = runner.invoke(report.report, [
                             './tests/test_files/dev_data/output.csv',
                             './tests/test_files/dev_data/dataset-dev.csv',
                             '-c', './tests/test_files/dev_data/config-dev.json'])
    assert response.exit_code == 0

    assert exists("./grouping_results_report.xlsx")
    wb = load_workbook("./grouping_results_report.xlsx")
    ws1 = wb["individual_report_1"]

    cell1_color = ws1[2][7].fill.start_color.index
    cell2_color = ws1[3][7].fill.start_color.index
    cell3_color = ws1[4][7].fill.start_color.index
    cell4_color = ws1[5][7].fill.start_color.index
    cell5_color = ws1[6][7].fill.start_color.index
    cell6_color = ws1[7][7].fill.start_color.index
    cell7_color = ws1[8][7].fill.start_color.index
    cell8_color = ws1[9][7].fill.start_color.index
    cell9_color = ws1[10][7].fill.start_color.index
    cell10_color = ws1[11][7].fill.start_color.index
    cell11_color = ws1[12][7].fill.start_color.index
    cell12_color = ws1[13][7].fill.start_color.index
    cell13_color = ws1[14][7].fill.start_color.index
    cell14_color = ws1[15][7].fill.start_color.index
    cell15_color = ws1[16][7].fill.start_color.index
    cell16_color = ws1[17][7].fill.start_color.index

    assert cell1_color == "FF00FF00"
    assert cell2_color == "FF00FF00" 
    assert cell3_color == "FF00FF00" 
    assert cell4_color == "FF00FF00"
    assert cell5_color == "FF00FF00"
    assert cell6_color == "FF00FF00" 
    assert cell7_color == "FF00FF00" 
    assert cell8_color == "FF00FF00"  
    assert cell9_color == "FF00FF00"
    assert cell10_color == "FF00FF00" 
    assert cell11_color == "FF00FF00" 
    assert cell12_color == "FF00FF00"
    assert cell13_color == "FF00FF00"
    assert cell14_color == "FF00FF00" 
    assert cell15_color == "FF00FF00" 
    assert cell16_color == "FF00FF00"

    os.remove("./grouping_results_report.xlsx")
    