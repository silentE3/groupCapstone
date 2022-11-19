from app.group import scoring
from app import models


def test_scoring_groups_1():
    # 2 disliked pairings, 0 groups without avail overlap, 300 preferred pairings
    # target group size = 5, preferred slots on survey = 3, number of students = 100
    # Note: This means max num groups possible = 25
    setdata = models.GroupSetData("group1", 0, 2, 300, 5, 3, 100)
    assert scoring.score_groups(setdata) == 1612


def test_scoring_groups_2():
    # 1 disliked pairings, 25 (all possible) groups without avail overlap, 0 preferred pairings
    # target group size = 5, preferred slots on survey = 3, number of students = 100
    # Note: This means max num groups possible = 25
    setdata = models.GroupSetData("group1", 25, 1, 0, 5, 3, 100)
    assert scoring.score_groups(setdata) == 1611


def test_scoring_groups_3():
    # invalid target group size of 0 should be automatically set to 1
    # 1 disliked pairings, 25 (all possible) groups without avail overlap, 0 preferred pairings
    # target group size = 1, preferred slots on survey = 3, number of students = 100
    # Note: This means max num groups possible = 100
    setdata = models.GroupSetData("group1", 25, 1, 0, 0, 3, 100)
    assert scoring.score_groups(setdata) == 3936


def test_scoring_single_group_1():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2'],
        disliked_students=['asurite3'],
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        }
    ), models.SurveyRecord(
        student_id="asurite2",
        preferred_students=['asurite1', 'asurite4'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite6'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    )])  # 2 preferred pairings, 1 disliked pairing, availability overlap
    # target group size = 2, preferred slots on survey = 2, number of students = 7
    # Note: This means max num groups possible = 7
    set_vars = models.GroupSetData(group.group_id, 0, 0, 0, 2, 2, 7)
    assert scoring.score_individual_group(group, set_vars) == 20.4


def test_scoring_single_group_2():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=[],
        disliked_students=['asurite3', 'asurite2'],
        availability={
            "1": [],
            "2": [],
            "3": [],
        }
    ), models.SurveyRecord(
        student_id="asurite2",
        preferred_students=['asurite1', 'asurite4'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite6'],
        disliked_students=['asurite1'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    )])  # 1 preferred pairings, 3 disliked pairing, no availability overlap
    # target group size = 2, preferred slots on survey = 2, number of students = 7
    # Note: This means max num groups possible = 7
    set_vars = models.GroupSetData(group.group_id, 0, 0, 0, 2, 2, 7)
    assert scoring.score_individual_group(group, set_vars) == 61.3


def test_scoring_single_group_3():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=[],
        disliked_students=['asurite3', 'asurite2'],
        availability={
            "1": [],
            "2": [],
            "3": [],
        }
    ), models.SurveyRecord(
        student_id="asurite2",
        preferred_students=['asurite1', 'asurite4'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite6'],
        disliked_students=['asurite1'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    )])  # 1 preferred pairings, 3 disliked pairing, no availability overlap
    # target group size = 3, preferred slots on survey = 3, number of students = 10
    # Note: This means max num groups possible = 5
    set_vars = models.GroupSetData(group.group_id, 0, 0, 0, 3, 3, 10)
    assert scoring.score_individual_group(group, set_vars) == 78.9


def test_standard_dev_groups():
    group_1 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2'],
        disliked_students=['asurite3'],
        availability={
            "1": ['monday'],
            "2": [],
            "3": [],
        }
    ), models.SurveyRecord(
        student_id="asurite2",
        preferred_students=['asurite1', 'asurite4'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    ), models.SurveyRecord(
        student_id="asurite3",
        preferred_students=['asurite6'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    )])  # 2 preferred pairings, 1 disliked pairing, availability overlap

    group_2 = models.GroupRecord("2", [models.SurveyRecord(
        student_id="asurite4",
        preferred_students=[],
        disliked_students=['asurite6', 'asurite5'],
        availability={
            "1": [],
            "2": [],
            "3": [],
        }
    ), models.SurveyRecord(
        student_id="asurite5",
        preferred_students=['asurite4', 'asurite7'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    ), models.SurveyRecord(
        student_id="asurite6",
        preferred_students=['asurite1'],
        disliked_students=['asurite4'],
        availability={
            "1": ['monday', 'tuesday'],
            "2": [],
            "3": ['wednesday'],
        }
    )])  # 1 preferred pairings, 3 disliked pairing, no availability overlap

    # target group size = 2, preferred slots on survey = 2, number of students = 7
    # Note: This means max num groups possible = 7
    # Score for group_1 = 20.4 and group_2 = 61.3
    # expected standard deviation = 20.45
    set_vars = models.GroupSetData("group_solution", 0, 0, 0, 2, 2, 7)
    assert scoring.standard_dev_groups([group_1, group_2], set_vars) == 20.45
