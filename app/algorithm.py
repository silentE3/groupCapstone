"""
module for the implementation of the grouping algorithm
"""
import copy
from random import randint
from app import models
from app.group import validate


class Algorithm:
    '''
    class with operations that perform the algorithm to group students
    '''

    def __init__(self, students) -> None:
        self.students: list[models.SurveyRecord] = students
        self.bad_students: list[models.SurveyRecord] = []
        self.groups: list[models.GroupRecord] = []
        self.max_group_size = len(self.students) // 5
        for idx in range(self.max_group_size):
            self.groups.append(models.GroupRecord(f"group_{idx+1}"))

    def group_students(self) -> list[models.GroupRecord]:
        """
        initiates the grouping process
        """
        while len(self.students) > 0:
            student = self.students.pop()
            self.add_student_to_group(student)
        self.fix_bad_groups()
        print(len(self.students))
        return self.groups

    def fix_bad_groups(self):
        '''
        fix bad groups looks at the groups that were created and attempts to fix them
        '''
        self.students.extend(self.bad_students)
        while len(self.students) > 0:
            student = self.students.pop()
            self.add_bad_student_to_group(student)

    def add_bad_student_to_group(self, student: models.SurveyRecord):
        """
        adds a student to a given group
        """
        for group in self.groups:
            if meets_hard_requirement(student, group):
                group.members.append(student)
                return

        scenarios = self.run_bad_scenarios(student, 6)
        if len(scenarios) == 0:
            print('no scenarios :(')
            return

        randidx = randint(0, len(scenarios)-1)
        chosen_scenario = scenarios.pop(randidx)
        for group in self.groups:
            if group.group_id == chosen_scenario.group.group_id:
                group.members = chosen_scenario.group.members
                if chosen_scenario.removed_user is not None:
                    self.students.append(chosen_scenario.removed_user)

    def add_student_to_group(self, student: models.SurveyRecord):
        """
        adds a student to a given group. Initially we just look to see that hard requirements are met.
        After that, we look for best case scenarios.
        This ensures population of the groups before getting hung up in a cycle of finding best case scenarios.
        """
        for group in self.groups:
            if meets_hard_requirement(student, group):
                group.members.append(student)
                return

        scenarios = self.run_scenarios(student, 5)
        if len(scenarios) == 0:
            self.bad_students.append(student)
            print('bad student len: ', len(self.bad_students))
            return

        target_scenario = scenarios.pop(0)
        matched_scenarios = [target_scenario]
        for scenario in scenarios:
            if scenario.score == target_scenario.score:
                matched_scenarios.append(scenario)

        randidx = randint(0, len(matched_scenarios)-1)
        chosen_scenario = matched_scenarios[randidx]
        for group in self.groups:
            if group.group_id == chosen_scenario.group.group_id:
                group.members = chosen_scenario.group.members
                if chosen_scenario.removed_user is not None:
                    self.students.append(chosen_scenario.removed_user)

    def run_scenarios(self, student, max_size):
        """
        runs all of the available scenarios for adding this user to a group
        """

        scenarios: list[models.Scenario] = []
        for group in self.groups:
            scenarios.extend(group_scenarios(student, group, max_size))

        scenarios.sort(reverse=True)

        return scenarios

    def run_bad_scenarios(self, student, max_size):
        """
        runs all of the available scenarios for adding this user to a group
        """

        scenarios: list[models.Scenario] = []
        for group in self.groups:
            scenarios.extend(group_scenarios_doesnt_have_to_be_better(
                student, group, max_size))

        scenarios.sort(reverse=True)

        return scenarios


def group_scenarios(student: models.SurveyRecord, group: models.GroupRecord, max_size: int):
    """
    creates scenarios for all possible situations with the group
    1. just adding the user to the group
    2. swapping the user for another

    returns a list of scenarios
    """
    scenarios: list[models.Scenario] = []
    if len(group.members) < max_size:
        group_new = copy.deepcopy(group)
        group_new.members.append(student)
        scenario = models.Scenario(group_new, rank_group(group_new))
        scenarios.append(scenario)

    if len(group.members) == max_size:
        for mem in group.members:
            group_new = copy.deepcopy(group)
            group_new.members.remove(mem)
            group_new.members.append(student)
            if rank_group(group) < rank_group(group_new):
                scenario = models.Scenario(group_new, rank_group(group_new), mem)
                scenarios.append(scenario)

    return scenarios


def group_scenarios_doesnt_have_to_be_better(student: models.SurveyRecord, group: models.GroupRecord, max_size: int):
    """
    creates scenarios for all possible situations with the group
    1. just adding the user to the group
    2. swapping the user for another

    returns a list of scenarios
    """
    scenarios: list[models.Scenario] = []
    if len(group.members) < max_size:
        group_new = copy.deepcopy(group)
        group_new.members.append(student)
        scenario = models.Scenario(group_new, rank_group(group_new))
        scenarios.append(scenario)

    if len(group.members) == max_size:
        for mem in group.members:
            group_new = copy.deepcopy(group)
            group_new.members.remove(mem)
            group_new.members.append(student)
            scenario = models.Scenario(group_new, rank_group(group_new), mem)
            scenarios.append(scenario)

    return scenarios


def rank_group(group: models.GroupRecord) -> int:
    '''
    how do we provide a number ranking to a group??
    1. dislikes = return a score of 0
    2. availability = add 100 to each
    3. preferred_occurrences = add 1 to each
    '''

    if len(validate.users_disliked_in_group(group)) > 0:
        return 0

    availability = validate.availability_overlap_count(group)
    if availability == 0:
        return 0

    preferred_users = validate.group_likes_count(group)

    return availability * 100 + preferred_users


def meets_hard_requirement(student: models.SurveyRecord, group: models.GroupRecord):
    '''
    checks if the basic hard requirements are met including the group size, availability, and dislikes
    '''
    group_copy = copy.deepcopy(group)
    group_copy.members.append(student)
    dislikes = validate.meets_dislike_requirement(group_copy)
    matches_avail = validate.meets_group_availability_requirement(group_copy)
    group_size = len(group_copy.members)

    return dislikes and matches_avail and group_size < 6


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
    '''
    creates a ranking for students based on their availability and # of people they are compatible with
    '''
    for student in students:
        student.avail_rank = total_availability_matches(student, students)
        student.okay_with_rank = len(
            students) - total_dislike_incompatible_students(student, students)

    students.sort(reverse=True)
