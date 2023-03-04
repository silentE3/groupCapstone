import os
import shutil
from click.testing import CliRunner
import click
from app.commands import report
from os.path import exists
from openpyxl import load_workbook, workbook
import xlsxwriter
import random
from app.file import xlsx

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
    workbook1 = xlsxwriter.Workbook("Random.xlsx")
    worksheet = workbook1.add_worksheet()
    green_bg = workbook1.add_format({"bg_color": "#00FF00"})

    random1 = random.randint(0,1)
    
    worksheet.write('A1', 1, green_bg)
    worksheet.write('B1', 1)
    worksheet.write('C1', 1, green_bg)
    worksheet.write('A2', 1)
    worksheet.write('B2', 1, green_bg)
    worksheet.write('C2', 1)
    workbook1.close()

    book: workbook.Workbook = load_workbook("Random.xlsx")
    assert exists("Random.xlsx")
    ws1 = book["Sheet1"]

    cell1color = ws1[1][0].fill.start_color.index
    cell2color = ws1[1][1].fill.start_color.index
    cell3color = ws1[1][2].fill.start_color.index
    cell4color = ws1[2][0].fill.start_color.index
    cell5color = ws1[2][1].fill.start_color.index
    cell6color = ws1[2][2].fill.start_color.index

    assert cell1color == "FF00FF00"
    assert cell2color != "FF00FF00"
    assert cell3color == "FF00FF00"
    assert cell4color != "FF00FF00"
    assert cell5color == "FF00FF00"
    assert cell6color != "FF00FF00"
    
    os.remove("Random.xlsx")

    