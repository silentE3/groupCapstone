"""
module for the implementation of the grouping algorithm
"""
import copy
from dataclasses import dataclass, field
from random import randint
from typing import Optional
from app import models
from app.group import validate


class Algorithm:

    def __init__(self, students) -> None:
        self.students: list[models.SurveyRecord] = students
        self.groups: list[models.GroupRecord] = []
        self.max_group_size = len(self.students) // 5
        for x in range(self.max_group_size):
            self.groups.append(models.GroupRecord(f"group_{x}"))

    def group_students(self) -> list[models.GroupRecord]:
        tries = 0
        while len(self.students) > 0 and tries < 20000:
            student = self.students.pop()
            self.add_student_to_group(student)
            tries += 1
        return self.groups

    def add_student_to_group(self, student: models.SurveyRecord):
        """adds a student to a given group

        1. loop through the groups
        2. Find a group that is open
        3. If there is an open group and the group meets the dislike+availability requirement, append them
        4. if no groups worked we need to look at adding a new group if it is an option.
        5. if we have made all of the groups, it is time to look at swapping the users
        """
        for group in self.groups:
            # first check if hard requirements are met. There is a group, the group meets size requirement, dislikes, and availability.
            if meets_hard_requirement(student, group):
                group.members.append(student)
                return
        scenarios = self.run_scenarios(student)

        if len(scenarios) == 0:
            raise Exception('no available grouping scenarios')

        target_scenario = scenarios.pop(0)
        matched_scenarios = [target_scenario]
        for s in scenarios:
            if s.score == target_scenario.score:
                matched_scenarios.append(s)

        randidx = randint(0, len(matched_scenarios)-1)

        chosen_scenario = matched_scenarios[randidx]

        for group in self.groups:
            if group.group_id == chosen_scenario.group.group_id:
                group.members = chosen_scenario.group.members
                if chosen_scenario.removed_user is not None:
                    self.students.append(chosen_scenario.removed_user)

    def run_scenarios(self, student):
        """
        runs all of the available scenarios for adding this user to a group
        """
        empty_ones_exist = 0
        for g in self.groups:
            if len(g.members) == 0:
                empty_ones_exist += 1

        scenarios: list[Scenario] = []
        for group in self.groups:
            scenarios.extend(group_scenarios(student, group))

        scenarios.sort(reverse=True)

        return scenarios


def group_scenarios(student: models.SurveyRecord, group: models.GroupRecord):
    """
    creates scenarios for all possible situations with the group
    1. just adding the user to the group
    2. swapping the user for another

    returns a list of scenarios
    """
    scenarios: list[Scenario] = []
    # check the scenario of just adding the member to the group
    if len(group.members) < 5:
        group_new = copy.deepcopy(group)
        group_new.members.append(student)
        scenario = Scenario(group_new, rank_group(group_new))
        scenarios.append(scenario)

    if len(group.members) == 5:
        for mem in group.members:
            group_new = copy.deepcopy(group)
            group_new.members.remove(mem)
            group_new.members.append(student)
            scenario = Scenario(group_new, rank_group(group_new), mem)
            scenarios.append(scenario)

    return scenarios


def rank_group(group: models.GroupRecord) -> int:
    '''
    how do we provide a number ranking to a group??
    start at 100
    1. dislikes = return a score of 0
    2. availability = add 100 to each
    3. preferred_occurrences = add 1 to each
    if score < 100 it is bad
    if score > 100 it is good
    '''

    if len(validate.users_disliked_in_group(group)) > 0:
        return 0

    availability = validate.availability_overlap_count(group)

    preferred_users = validate.group_likes_count(group)

    return availability * 100 + preferred_users


def meets_hard_requirement(student, group):
    dislikes = validate.user_dislikes_group(student, group)
    matches_avail = validate.user_matches_availability_count(student, group)
    group_size = len(group.members)
    
    return dislikes == 0 and matches_avail > 0 and group_size < 6


def total_dislike_incompatible_students(student: models.SurveyRecord, students: list[models.SurveyRecord]) -> int:
    """
    function to identify the total number of students that are disliked
    This should be the total count of incompatible students for the student.
    If the dislike is reciprical, don't count it twice.

    Args:
        student (models.SurveyRecord): student to check
        students (list[models.SurveyRecord]): full list of students

    Returns:
        int: number of total incompatible students
    """
    disliked_set: set[str] = set(student.disliked_students)

    for other_student in students:
        if student.student_id == other_student.student_id:
            continue

        if student.student_id in other_student.disliked_students:
            disliked_set.add(other_student.student_id)

    return len(disliked_set)


def total_availability_matches(student: models.SurveyRecord, students: list[models.SurveyRecord]) -> int:
    """
    checks the student's availability against everyone elses and counts the number of times that they match

    Args:
        student (models.SurveyRecord): student to check matches for
        students (list[models.SurveyRecord]): full list of students

    Returns:
        int: number of times the student matches availability in the dataset
    """

    totals = 0

    for other_student in students:
        if student.student_id == other_student.student_id:
            continue

        for time, avail_days in other_student.availability.items():
            for avail_day in avail_days:
                if avail_day in student.availability[time] and not avail_day == '':
                    totals += 1

    return totals


def rank_students(students: list[models.SurveyRecord]):
    for student in students:
        student.avail_rank = total_availability_matches(student, students)
        student.okay_with_rank = len(
            students) - total_dislike_incompatible_students(student, students)

    students.sort(reverse=True)


def group_scenario_rank(student: models.SurveyRecord, group: models.GroupRecord):
    totals = 0

    if len(validate.user_dislikes_group(student, group)):
        return 0

    totals += validate.user_matches_availability_count(student, group)

    totals += len(validate.user_likes_group(student, group)) * 0.5

    return totals


@dataclass
class Scenario:
    group: models.GroupRecord
    score: int
    removed_user: Optional[models.SurveyRecord] = field(default=None)

    def __lt__(self, other):
        return self.score < other.score
