'''
Tests general core grouping functionality
'''

from app import models
from app import core


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

    target_group_size: int = -1
    target_plus_one_allowed: bool = True
    target_minus_one_allowed: bool = True

    assert core.pre_group_error_checking(
        target_group_size, target_plus_one_allowed, target_minus_one_allowed, group) == True


def test_pre_group_error_checking_invalid_target_2():
    '''
    Verify True (error) returned for a valid list of students but with an
    invalid target group size (<=0).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    )]

    target_group_size = 0
    target_plus_one_allowed: bool = True
    target_minus_one_allowed: bool = True

    assert core.pre_group_error_checking(
        target_group_size, target_plus_one_allowed, target_minus_one_allowed, group) == True


def test_pre_group_error_checking_invalid_list():
    '''
    Verify True (error) returned for an invalid (empty) list of students but with a
    valid target group size (>0).
    '''

    group = []

    target_group_size = 1
    target_plus_one_allowed: bool = True
    target_minus_one_allowed: bool = True

    assert core.pre_group_error_checking(
        target_group_size, target_plus_one_allowed, target_minus_one_allowed, group) == True


def test_pre_group_error_checking_invalid_list_and_target():
    '''
    Verify True (error) returned for an invalid (empty) list of students and an
    invalid target group size (<=0).
    '''

    group = []

    target_group_size = 0
    target_plus_one_allowed: bool = True
    target_minus_one_allowed: bool = True

    assert core.pre_group_error_checking(
        target_group_size, target_plus_one_allowed, target_minus_one_allowed, group) == True


def test_pre_group_error_checking_valid_1():
    '''
    Verify False (no error) returned for an valid (non-empty) list of students and a
    valid target group size (>0).
    '''

    group = [models.SurveyRecord(
        student_id="asurite1",
    )]

    target_group_size = 1
    target_plus_one_allowed: bool = True
    target_minus_one_allowed: bool = True

    assert core.pre_group_error_checking(
        target_group_size, target_plus_one_allowed, target_minus_one_allowed, group) == False


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
    target_plus_one_allowed: bool = True
    target_minus_one_allowed: bool = True

    assert core.pre_group_error_checking(
        target_group_size, target_plus_one_allowed, target_minus_one_allowed, group) == False


def test_get_min_max_num_groups():
    '''
    This method tests the updated get_min_max_num_groups.
    '''
    group = [models.SurveyRecord(
        student_id="asurite1",
    ), models.SurveyRecord(
        student_id="asurite2",
    ), models.SurveyRecord(
        student_id="asurite3",
    ), models.SurveyRecord(
        student_id="asurite4",
    )]

    group2 = [models.SurveyRecord(
        student_id="asurite5",
    ), models.SurveyRecord(
        student_id="asurite6",
    ), models.SurveyRecord(
        student_id="asurite7",
    ), models.SurveyRecord(
        student_id="asurite8",
    )]