from app.group import scoring, scoring_alternative
from app.group.scoring import standard_dev_groups
from app import models


def test_scoring_alternative_groups_1():
    # 2 disliked pairings, 25 groups (all possible) without avail overlap, 300 preferred pairings, 175 additional overlapping slots, 0 students without a preferred pairing
    # target group size = 5, preferred slots on survey = 3, number of students = 100, time slots on survey = 8
    # Note: This means max num groups possible = 25
    setdata = models.GroupSetData("group1",
                                  target_group_size=5,
                                  num_survey_preferred_slots=3,
                                  num_students=100,
                                  num_survey_time_slots=8,
                                  num_groups_no_overlap=0,
                                  num_disliked_pairs=2,
                                  num_preferred_pairs=300,
                                  num_additional_overlap=175,
                                  num_students_no_pref_pairs=0,
                                  num_additional_pref_pairs=200)
    assert scoring_alternative.score_groups(setdata) == -704.425


def test_scoring_alternative_groups_2():
    # 1 disliked pairings, 25 (all possible) groups without avail overlap, 0 preferred pairings, 0 additional overlapping slots, 100 students (all) w/o a preferred pairing
    # target group size = 5, preferred slots on survey = 3, number of students = 100, time slots on survey = 8, num groups = 25
    # Note: This means max num groups possible = 25
    setdata = models.GroupSetData("group1",
                                  target_group_size=5,
                                  num_survey_preferred_slots=3,
                                  num_students=100,
                                  num_survey_time_slots=8,
                                  num_groups_no_overlap=25,
                                  num_disliked_pairs=1,
                                  num_preferred_pairs=0,
                                  num_additional_overlap=0,
                                  num_students_no_pref_pairs=100,
                                  num_additional_pref_pairs=0)
    assert scoring_alternative.score_groups(setdata) == -703.5


def test_scoring_alternative_groups_3():
    # invalid target group size of 0 should be automatically set to 1
    # 1 disliked pairings, 55 groups without avail overlap, 12 preferred pairings, 18 additional overlapping slots, 90 students w/o a preferred pairing
    # target group size = 1, preferred slots on survey = 4, number of students = 100, time slots on survey = 6
    # Note: This means max num groups possible = 100
    setdata = models.GroupSetData("group1",
                                  target_group_size=0,
                                  num_survey_preferred_slots=4,
                                  num_students=100,
                                  num_survey_time_slots=6,
                                  num_groups_no_overlap=55,
                                  num_disliked_pairs=1,
                                  num_preferred_pairs=12,
                                  num_additional_overlap=18,
                                  num_students_no_pref_pairs=90,
                                  num_additional_pref_pairs=2)
    assert scoring_alternative.score_groups(setdata) == -2096.498


def test_scoring_alternative_single_group_1():
    group = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2'],
        disliked_students=['asurite3'],
        availability={
            "1": ['monday'],
            "2": [],
            "3": ['wednesday'],
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
    )])  # 2 preferred pairings, 1 disliked pairing, 0 groups without availability overlap, 1 additional time slots, 1 student w/o a preferred pairing
    # target group size = 2, preferred slots on survey = 2, number of students = 7, time slots on survey = 6
    # Note: This means max num groups possible = 7
    set_vars = models.GroupSetData(group.group_id,
                                   target_group_size=2,
                                   num_survey_preferred_slots=2,
                                   num_students=7,
                                   num_survey_time_slots=6)
    assert scoring.score_individual_group(
        group, set_vars, True) == -14.5982


def test_scoring_alternative_single_group_2():
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
        preferred_students=['asurite1', 'asurite3'],
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
    )])  # 2 preferred pairings, 3 disliked pairing, no availability overlap (which means no additional overlap), 2 students w/o a preferred pairing
    # target group size = 2, preferred slots on survey = 2, number of students = 7, time slots on survey = 6
    # Note: This means max num groups possible = 7
    set_vars = models.GroupSetData(group.group_id, 2, 2, 7, 6)
    assert scoring.score_individual_group(
        group, set_vars, True) == -43.5982


def test_scoring_alternative_single_group_3():
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
    )])  # 1 preferred pairings, 3 disliked pairing, no availability overlap (which means no additional overlap), 2 student w/o a preferred pairing
    # target group size = 3, preferred slots on survey = 3, number of students = 10, time slots on survey = 4
    # Note: This means max num groups possible = 5
    set_vars = models.GroupSetData(group.group_id, 3, 3, 10, 4)
    assert scoring.score_individual_group(group, set_vars, True) == -52.1


def test_scoring_alternative_std_dev_groups():
    group_1 = models.GroupRecord("1", [models.SurveyRecord(
        student_id="asurite1",
        preferred_students=['asurite2'],
        disliked_students=['asurite3'],
        availability={
            "1": ['monday'],
            "2": [],
            "3": ['wednesday'],
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
    )])  # 2 preferred pairings, 1 disliked pairing, availability overlap, 1 "additional" overlap

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

    # target group size = 2, preferred slots on survey = 2, number of students = 7, time slots on survey = 6
    # Note: This means max num groups possible = 7
    # Score for group_1 = -14.5982 and group_2 = -43.6
    # expected standard deviation = 14.5009
    set_vars = models.GroupSetData("group_solution", 2, 2, 7, 6)
    assert round(standard_dev_groups(
        [group_1, group_2], set_vars, True), 4) == 14.5009
