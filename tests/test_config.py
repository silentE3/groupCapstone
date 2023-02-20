'''
Tests reading in a configuration file 
'''
# Note: Only verification of the group size parameter is specifically covered here at this time.

from app import config
from app.models import Configuration


def test_config_target_group_size_2():
    '''
    Config with a target group size of 2.
    '''
    expected_target_group_size = 2
    configuration = config.read_json(
        "./tests/test_files/configs/config_1.json")
    assert configuration["target_group_size"] == expected_target_group_size


def test_config_target_group_size_7():
    '''
    Config with a target group size of 7.
    '''
    expected_target_group_size = 7
    configuration = config.read_json(
        "./tests/test_files/configs/config_4.json")
    assert configuration["target_group_size"] == expected_target_group_size


def test_config_target_group_size_0():
    '''
    Config with a target group size of 0.
    '''
    expected_target_group_size = 0
    configuration = config.read_json(
        "./tests/test_files/configs/config_zero_group_size.json")
    assert configuration["target_group_size"] == expected_target_group_size


def test_config_target_group_size_negative():
    '''
    Config with a target group size of -1.
    '''
    expected_target_group_size = -1
    configuration = config.read_json(
        "./tests/test_files/configs/config_negative_group_size.json")
    assert configuration["target_group_size"] == expected_target_group_size

def test_read_report_config():
    '''
    Tests if the config file properly reads the config tab in the report and gets the columns
    holding only 1 row value.
    '''
    result:Configuration = config.read_report_config("Example_Report_1.xlsx")

    assert result.get("class_name") == "SER401"
    assert result.get("target_group_size") == 2
    assert result.get("target_plus_one_allowed") == True
    assert result.get("target_minus_one_allowed") == False
    assert result.get("availability_values_delimiter") == ";,"

def test_read_report_config_2():
    '''
    Tests if the config file properly reads the config tab in the report and gets the columns
    holding more than 1 row value.
    '''
    result:Configuration = config.read_report_config("Example_Report_1.xlsx")

    list = result.get("field_mappings")
    preferred_list = list.get("preferred_students_field_names")
    
    assert preferred_list[0] == "Preferred team member 1"
    assert preferred_list[1] == "Preferred team member 2"
    assert preferred_list[2] == "Preferred team member 3"
    assert preferred_list[3] == "Preferred team member 4"
    assert preferred_list[4] == "Preferred team member 5"
