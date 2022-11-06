'''
Tests reading in a configuration file 
'''
# Note: Only verification of the group size parameter is specifically covered here at this time.

from app import config


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
