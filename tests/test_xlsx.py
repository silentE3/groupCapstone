'''
test cases for the xlsx writer
'''
import os
from unittest.mock import patch
from app.file import xlsx
import pytest


def test_new_sheet_creates_sheet():
    '''
    tests that a sheet is created and it matches the name that was passed in
    '''
    writer = xlsx.XLSXWriter()
    assert writer.sheets == {}

    writer.new_sheet('sheet_uno')

    assert writer.sheets.get('sheet_uno')
    assert writer.sheets['sheet_uno'].get_name() == 'sheet_uno'


def test_new_sheet_duplicate_name_fails():
    '''
    tests that trying to create duplicate sheet name fails
    '''
    writer = xlsx.XLSXWriter()

    writer.new_sheet('sheet_uno')
    with pytest.raises(Exception):
        writer.new_sheet('sheet_uno')
        
def test_write_sheet_creates_sheet_if_not_exists():
    writer = xlsx.XLSXWriter()
    
    writer.write_sheet('sheet1', [[xlsx.Cell('test')]])

    assert writer.sheets.get('sheet1')
    
def test_save():
    writer = xlsx.XLSXWriter('test_groups.xlsx')
    
    writer.save()
    
    assert os.stat('test_groups.xlsx')
    
    os.remove('test_groups.xlsx')
