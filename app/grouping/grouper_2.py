"""
module for an additional grouping algorithm implementation
"""
import copy
from random import randint
from app import models
from app.data import load
from app.group import validate, scoring
from app.grouping import printer


class Grouper2:
    '''
    class with operations that perform an algorithm to group students
    '''

    def __init__(self, students, config, group_count: int) -> None:
        self.students: list[models.SurveyRecord] = copy.deepcopy(students)
        self.bad_students: list[models.SurveyRecord] = []
        self.groups: list[models.GroupRecord] = []
        self.group_count = group_count
        self.target_group_size = config['target_group_size']
        self.target_group_margin = 1
        self.grouping_passes = config['grouping_passes']
        self.config = config
        self.num_students: int = len(self.students)
        for idx in range(self.group_count):
            self.groups.append(models.GroupRecord(f"group_{idx+1}"))
        self.console_printer: printer.GroupingConsolePrinter = printer.GroupingConsolePrinter()

    def group_students(self) -> list[models.GroupRecord]:
        """
        initiates the grouping process
        """

        while len(self.students) > 0:
            student = self.students.pop()
            self.add_student_to_group(student)
        self.console_printer.print('balancing groups that need more members')
        self.balance_groups()
        self.console_printer.print('optimizing groups for best solution')
        self.optimize_groups()
        # self.console_printer.print(f'group size={self.group_count}, score={self.grade_groups()}')

        # Clear any final print statement in preparation for it to be overwritten
        self.console_printer.print("")
        return self.groups

    def balance_groups(self):
        '''
        balances groups
        '''
        for group in self.groups:
            if len(group.members) < self.target_group_size - self.target_group_margin:
                self.console_printer.print(
                    f'balancing group: {group.group_id} with size {len(group.members)}')
                self.balance_group(group)

    def balance_group(self, group: models.GroupRecord):
        '''
        balancing group to ensure there are enough members
        '''
        groups_with_enough_mems = list(filter(lambda group: len(
            group.members) > self.target_group_size-self.target_group_margin, self.groups))
        while len(group.members) < self.target_group_size-self.target_group_margin:
            for other_group in groups_with_enough_mems:
                for member in other_group.members:
                    if meets_hard_requirement(member, group, self.target_group_size):
                        other_group.members.remove(member)
                        group.members.append(member)
                        if len(other_group.members) <= self.target_group_size-self.target_group_margin:
                            groups_with_enough_mems.remove(other_group)
                        break
                if len(group.members) >= self.target_group_size-self.target_group_margin:
                    break
            for other_group in groups_with_enough_mems:
                member = other_group.members.pop()
                if len(other_group.members) <= self.target_group_size-self.target_group_margin:
                    groups_with_enough_mems.remove(other_group)
                group.members.append(member)
                break

    def optimize_groups(self):
        '''
        creates grouping optimizations by swapping users
        if 5 operations result in the same score, it will end with the assumption that it has done the best it will do
        '''
        prev_score = 0
        dup_score_count = 0
        for group_pass in range(self.grouping_passes):
            if prev_score == self.grade_groups():
                dup_score_count += 1
            else:
                dup_score_count = 1

            if dup_score_count >= 15:
                break

            prev_score = self.grade_groups()
            # self.console_printer.print(self.grade_groups())
            self.console_printer.print(f'optimization pass #{group_pass+1}')
            for group in self.groups:
                for mem in group.members:
                    scenario = self.run_swap_scenarios(group, mem)
                    if scenario is None:
                        continue
                    for other_group in self.groups:
                        if other_group.group_id == scenario.group_1.group_id:
                            other_group.members = scenario.group_1.members
                        elif other_group.group_id == scenario.group_2.group_id:
                            other_group.members = scenario.group_2.members
                    break

    def grade_groups(self):
        '''
        computes the score of the overall grouping
        '''
        num_pairings_disliked: int = validate.total_disliked_pairings(
            self.groups)
        num_groups_no_avail: int = validate.total_groups_no_availability(
            self.groups)
        num_pairings_liked: int = validate.total_liked_pairings(self.groups)
        num_additional_overlap: int = sum(
            # subtract one to get "additional"
            max(validate.availability_overlap_count(group) - 1, 0) for group in self.groups)

        scoring_vars = models.GroupSetData("solution_2",
                                           self.target_group_size,
                                           len((self.config["field_mappings"])[
                                               "preferred_students_field_names"]),
                                           self.num_students,
                                           len((self.config["field_mappings"])[
                                               "availability_field_names"]),
                                           num_groups_no_avail,
                                           num_pairings_disliked,
                                           num_pairings_liked,
                                           num_additional_overlap)
        return scoring.score_groups(scoring_vars)

    def add_student_to_group(self, student: models.SurveyRecord):
        """
        adds a student to a given group. Initially we just look to see that hard requirements are met.
        After that, we look for best case scenarios.
        This ensures population of the groups before getting hung up in a cycle of finding best case scenarios.
        """
        for group in self.groups:
            if meets_hard_requirement(student, group, self.target_group_size):
                group.members.append(student)
                return

        # if finding a scenario with the target group size isn't feasible, attempt to just append them
        for group in self.groups:
            if meets_hard_requirement(student, group, self.target_group_size+self.target_group_margin):
                group.members.append(student)
                return

        # starts running scenarios for swapping a student into another's spot
        scenarios = self.run_scenarios(student)
        if len(scenarios) > 0:
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
                        return
            return

        # if all else fails, just find an open group and add them
        for group in self.groups:
            if len(group.members) < self.target_group_size+self.target_group_margin:
                group.members.append(student)
                return

        # if we made it here, all of the groups are full
        self.console_printer.print(
            f'unable to group student with id: {student.student_id}')

    def run_scenarios(self, student):
        """
        runs all of the available scenarios for adding this user to a group
        """

        scenarios: list[models.Scenario] = []
        for group in self.groups:
            scenarios.extend(self.group_scenarios(student, group))

        scenarios.sort(reverse=True)

        return scenarios

    def run_swap_scenarios(self, group: models.GroupRecord, student: models.SurveyRecord):
        '''
        gives a list of scenarios if the student were to be swapped for another group.
        '''

        scenarios: list[models.SwapScenario] = []
        for other_group in self.groups:
            if group.group_id == other_group.group_id:
                continue
            copy_group = copy.deepcopy(group)
            scenarios.extend(self.swap_members_and_rate(
                student, copy_group, other_group))
        scenarios.sort(reverse=True)

        if len(scenarios) > 1:
            best_scenario = scenarios[0]
            for scenario in scenarios:
                if scenario.score1 + scenario.score2 >= best_scenario.score1 + best_scenario.score2:
                    best_scenario = scenario
            return best_scenario

        return None

    def swap_members_and_rate(self, student: models.SurveyRecord, group: models.GroupRecord, other_group: models.GroupRecord):
        '''
        removes the student from the group and checks adding them to the other group with certain members removed
        '''

        scenarios: list[models.SwapScenario] = []
        for member in other_group.members:
            oth_group_copy = copy.deepcopy(other_group)
            oth_group_copy.members.remove(member)
            oth_group_copy.members.append(student)
            group_copy = copy.deepcopy(group)
            group_copy.members.remove(student)
            group_copy.members.append(member)
            score_1 = self.rank_group(group_copy)
            score_2 = self.rank_group(oth_group_copy)

            if score_1 + score_2 >= self.rank_group(group) + self.rank_group(other_group):
                scenario = models.SwapScenario(
                    group_copy, oth_group_copy, score_1, score_2)
                scenarios.append(scenario)

        return scenarios

    def group_scenarios(self, student: models.SurveyRecord, group: models.GroupRecord):
        """
        creates scenarios for all possible situations with the group
        """
        scenarios: list[models.Scenario] = []
        for mem in group.members:
            group_new = copy.deepcopy(group)
            group_new.members.remove(mem)
            group_new.members.append(student)
            score = self.rank_group(group_new)
            if self.rank_group(group) < score and score >= 0:
                scenario = models.Scenario(
                    group_new, score, mem)
                scenarios.append(scenario)

        return scenarios

    def rank_group(self, group: models.GroupRecord) -> float:
        '''
        uses the scoring algorithm to rank the group
        '''
        scoring_vars = models.GroupSetData(group.group_id,
                                           self.config["target_group_size"],
                                           len((self.config["field_mappings"])[
                                               "preferred_students_field_names"]),
                                           self.num_students,
                                           len((self.config["field_mappings"])[
                                               "availability_field_names"]))
        return scoring.score_individual_group(group, scoring_vars)


def meets_hard_requirement(student: models.SurveyRecord, group: models.GroupRecord, max_group_size: int):
    '''
    checks if the basic hard requirements are met including the group size, availability, and dislikes
    '''
    group_copy = copy.deepcopy(group)
    group_copy.members.append(student)
    meets_dislikes = validate.meets_dislike_requirement(group_copy)
    meets_avail = validate.meets_group_availability_requirement(group_copy)
    group_size = len(group_copy.members)

    return meets_dislikes and meets_avail and group_size <= max_group_size


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


def rank_students(students: list[models.SurveyRecord]):
    '''
    creates a ranking for students based on their availability and # of people they are compatible with
    '''
    for student in students:
        student.avail_rank = load.total_availability_matches(student, students)
        student.okay_with_rank = len(
            students) - total_dislike_incompatible_students(student, students)

    students.sort(reverse=True)