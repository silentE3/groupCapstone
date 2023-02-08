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
    This method tests the updated get_min_max_num_groups with a fix group size.
    Note: survey data is models.SurveyRecord
    '''

    student1 = models.SurveyRecord(
        student_id="asurite1",
    )
    student2 = models.SurveyRecord(
        student_id="asurite2",
    )
    student3 = models.SurveyRecord(
        student_id="asurite3",
    )
    student4 = models.SurveyRecord(
        student_id="asurite4",
    )
    student5 = models.SurveyRecord(
        student_id="asurite5",
    )
    student6 = models.SurveyRecord(
        student_id="asurite6",
    )
    student7 = models.SurveyRecord(
        student_id="asurite7",
    )
    student8 = models.SurveyRecord(
        student_id="asurite8",
    )
    
    students = []
    students.append(student1)
    students.append(student2)
    students.append(student3)
    students.append(student4)
    students.append(student5)
    students.append(student6)
    students.append(student7)
    students.append(student8)

    output = core.get_min_max_num_groups(students, 4, False, False)
    print(output)

    min = output[0]
    max = output[1]

    assert min == 2
    assert max == 2

def test_get_min_max_num_groups_2():
    '''
    This method tests the updated get_min_max_num_groups with plus one being true.
    Note: survey data is models.SurveyRecord
    '''
    student1 = models.SurveyRecord(
        student_id="asurite1",
    )
    student2 = models.SurveyRecord(
        student_id="asurite2",
    )
    student3 = models.SurveyRecord(
        student_id="asurite3",
    )
    student4 = models.SurveyRecord(
        student_id="asurite4",
    )
    student5 = models.SurveyRecord(
        student_id="asurite5",
    )
    student6 = models.SurveyRecord(
        student_id="asurite6",
    )
    student7 = models.SurveyRecord(
        student_id="asurite7",
    )
    student8 = models.SurveyRecord(
        student_id="asurite8",
    )
    student9 = models.SurveyRecord(
        student_id="asurite9",
    )
    student10 = models.SurveyRecord(
        student_id="asurite10",
    )

    students = []
    students.append(student1)
    students.append(student2)
    students.append(student3)
    students.append(student4)
    students.append(student5)
    students.append(student6)
    students.append(student7)
    students.append(student8)
    students.append(student9)
    students.append(student10)

    output = core.get_min_max_num_groups(students, 3, True, False)
    print(output)

    min = output[0]
    max = output[1]

    assert min == 3
    assert max == 3

def test_get_min_max_num_groups_3():
    '''
    This method tests the updated get_min_max_num_groups with minus one being true.
    Note: survey data is models.SurveyRecord
    '''
    student1 = models.SurveyRecord(
        student_id="asurite1",
    )
    student2 = models.SurveyRecord(
        student_id="asurite2",
    )
    student3 = models.SurveyRecord(
        student_id="asurite3",
    )
    student4 = models.SurveyRecord(
        student_id="asurite4",
    )
    student5 = models.SurveyRecord(
        student_id="asurite5",
    )
    student6 = models.SurveyRecord(
        student_id="asurite6",
    )
    student7 = models.SurveyRecord(
        student_id="asurite7",
    )

    students = []
    students.append(student1)
    students.append(student2)
    students.append(student3)
    students.append(student4)
    students.append(student5)
    students.append(student6)
    students.append(student7)

    output = core.get_min_max_num_groups(students, 4, False, True)
    print(output)

    min = output[0]
    max = output[1]

    assert min == 2
    assert max == 2