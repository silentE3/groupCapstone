'''
Tests general core grouping functionality
'''

from app import models
from app import core, config
from app.data.load import SurveyDataReader

def test_get_num_groups_1():
    '''
    Verify 3 groups for grouping of 6 students with a target group size of 2 (divides evenly).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
    )]

    target_group_size = 2
    expected_num_groups = 3

    assert core.get_num_groups(group, target_group_size) == expected_num_groups


def test_get_num_groups_2():
    '''
    Verify 2 groups for grouping of 8 students with a target group size of 5 (does
    not divide evenly, but still possible to maintain +/- 1 with rounding UP to 2 groups).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    ), models.SurveyRecord(
        student_id="asurite8",
    )]

    target_group_size = 5
    expected_num_groups = 2

    assert core.get_num_groups(group, target_group_size) == expected_num_groups


def test_get_num_groups_3():
    '''
    Verify 1 group for grouping of 8 students with a target group size of 7 (does
    not divide evenly, but still possible to maintain +/- 1 with rounding DOWN to 1 group).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    ), models.SurveyRecord(
        student_id="asurite8",
    )]

    target_group_size = 7
    expected_num_groups = 1

    assert core.get_num_groups(group, target_group_size) == expected_num_groups


def test_get_num_groups_invalid_1():
    '''
    Verify -1 groups (indicating "not possible") returned for grouping of 8 students 
    with a target group size of 6 (not possible to maintain +/- 1 of target group size).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    ), models.SurveyRecord(
        student_id="asurite8",
    )]

    target_group_size = 6
    expected_num_groups = -1

    assert core.get_num_groups(group, target_group_size) == expected_num_groups


def test_get_num_groups_zero_target():
    '''
    Verify 7 groups returned for grouping of 7 students with a target group 
    size of 0 (target of <= 0 automatically set to 1 by the function).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    )]

    target_group_size = 0
    expected_num_groups = 7

    assert core.get_num_groups(group, target_group_size) == expected_num_groups


def test_get_num_groups_negative_target():
    '''
    Verify 7 groups returned for grouping of 7 students with a target group 
    size of -1 (target of <= 0 automatically set to 1 by the function).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    )]

    target_group_size = -1
    expected_num_groups = 7

    assert core.get_num_groups(group, target_group_size) == expected_num_groups


def test_pre_group_error_checking_invalid_target_1():
    '''
    Verify True (error) returned for a valid list of students but with an
    invalid target group size (<=0).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    )]

    target_group_size = -1

    assert core.pre_group_error_checking(target_group_size, group) == True


def test_pre_group_error_checking_invalid_target_2():
    '''
    Verify True (error) returned for a valid list of students but with an
    invalid target group size (<=0).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    )]

    target_group_size = 0

    assert core.pre_group_error_checking(target_group_size, group) == True


def test_pre_group_error_checking_invalid_list():
    '''
    Verify True (error) returned for an invalid (empty) list of students but with a
    valid target group size (>0).
    '''

    group = []

    target_group_size = 1

    assert core.pre_group_error_checking(target_group_size, group) == True


def test_pre_group_error_checking_invalid_list_and_target():
    '''
    Verify True (error) returned for an invalid (empty) list of students and an
    invalid target group size (<=0).
    '''

    group = []

    target_group_size = 0

    assert core.pre_group_error_checking(target_group_size, group) == True


def test_pre_group_error_checking_valid_1():
    '''
    Verify False (no error) returned for an valid (non-empty) list of students and a
    valid target group size (>0).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    )]

    target_group_size = 1

    assert core.pre_group_error_checking(target_group_size, group) == False


def test_pre_group_error_checking_valid_2():
    '''
    Robustness test with more "reasonable" student list and target group sizes.
    Verify False (no error) returned for an valid (non-empty) list of students and a
    valid target group size (>0).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    ), models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    ), models.SurveyRecord(
        student_id="asurite8",
    )]

    target_group_size = 4

    assert core.pre_group_error_checking(target_group_size, group) == False

def test_multi_size_group_numbering_1():
    '''
    Tests the multi-size group sizing algorithm
    '''
    
    config_data: models.Configuration = config.read_json("./tests/test_files/configs/config_1.json")
    survey_reader = SurveyDataReader(config_data['field_mappings'])
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_1.csv')

    group_sizes: list[int] = core.get_group_sizes(surveys_result, config_data["target_group_size"])

    assert len(group_sizes) == 2
    assert group_sizes[0] == 2
    assert group_sizes[1] == 2

def test_multi_size_group_numbering_2():
    '''
    Tests the multi-size group sizing algorithm
    '''
    
    config_data: models.Configuration = config.read_json("./tests/test_files/configs/config_5.json")
    survey_reader = SurveyDataReader(config_data['field_mappings'])
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_5.csv')

    group_sizes: list[int] = core.get_group_sizes(surveys_result, config_data["target_group_size"])

    assert len(group_sizes) == 2
    assert group_sizes[0] == 5
    assert group_sizes[1] == 3


def test_multi_size_group_numbering_3():
    '''
    Tests the multi-size group sizing algorithm
    '''
    
    config_data: models.Configuration = config.read_json("./tests/test_files/configs/config_1.json")
    survey_reader = SurveyDataReader(config_data['field_mappings'])
    surveys_result = survey_reader.load('./tests/test_files/survey_results/Example_Survey_Results_2.csv')

    group_sizes: list[int] = core.get_group_sizes(surveys_result, config_data["target_group_size"])

    assert len(group_sizes) == 3
    assert group_sizes[0] == 2
    assert group_sizes[1] == 2
    assert group_sizes[2] == 2