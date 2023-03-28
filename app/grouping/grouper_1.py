'''
module for a grouping algorithm implementation that creates groups via a constructive, 
    heuristic approach with local backtracking.
'''

from copy import deepcopy
import random as rnd
from app import models
from app.group import validate
from app.group import scoring
from app.grouping import printer


class Grouper1:
    '''
    This class is used to create groups via a constructive, heuristic approach with local backtracking.
    '''
    survey_data: list[models.SurveyRecord]
    config_data: models.Configuration
    cur_sol_score: float
    scoring_vars: models.GroupSetData
    groups: list[models.GroupRecord]
    best_solution_found: list[models.GroupRecord]
    best_solution_score: float
    num_groups: int
    console_printer: printer.GroupingConsolePrinter

    def __init__(self, survey_data: list[models.SurveyRecord], config_data: models.Configuration,
                 num_groups: int, console_printer: printer.GroupingConsolePrinter):
        self.survey_data = survey_data
        self.config_data = config_data
        self.groups = []
        self.best_solution_found = []
        self.best_solution_score = -1
        self.num_groups = num_groups
        self.console_printer = console_printer

    def create_groups(self) -> object:
        '''
        Method for grouping students via a constructive, heuristic approach with local
            backtracking, as follows:
            Step 1: Pre-process Student List
                The student list is sorted based on number of dislikes, with those having
                    the most dislikes at the top of the list. This should improve performance of
                    the algorithm by forcing “difficult” students (those with a lot of dislikes) to
                    be grouped first.
                Note: some randomization is included within this list by randomizing the order of
                    students with the same number of dislikes. This means that each grouping_pass
                    can/should produce different results.
            Step 2: Construct Initial Groups
                Initial groups are formed by adding each student to a group one at a time from
                    the list generated in step 1 (top to bottom).
                When considering which group to add a student to, the disliked pairings and
                    availability overlap constraints are considered, and an attempt at
                    minimizing violations of these constrains is made.
            Step 3: Perform Local Backtracking, Phase 1
                Now that a solution group set exists (from step 2), local backtracking is performed
                    in an attempt to improve the solution.
                First, an attempt to eliminate disliked pairings is made by swapping students that
                    are part of such pairings into other groups.
                Second, an attempt to eliminate groups without an overlapping time slot is made by
                    swapping key students into other groups.
                NOTE: At each backtracking step, considered swaps are only performed if they
                    are found to improve or at least not decrease the solution's score.
            Step 4: Save the Current "Optimal" Solution
                Compare the score of the solution produced by Step 3 to that of any currently saved
                “optimal” solution (from previous Step 1-4 runs, if applicable) and save whichever
                has a higher score.
            Step 5: Repeat Steps 1-4 "grouping_passes" number of times (specified in the config)
            Step 6: Perform Local Backtracking, Phase 2
                An attempt to increase the number of preferred pairings and "additional" overlapping
                    availability is made by swapping students between groups.
                NOTE: Considered swaps will only be performed if they
                    are found to improve or at least not decrease the solution's score.
        '''

        # "Step 5": Repeat Steps 1-4 "grouping_passes" number of times (specified in the config)
        for grouping_pass in range(max(self.config_data["grouping_passes"], 1)):
            self.groups = []
            # Steps 1 thru 4
            self.__start_grouping(grouping_pass, self.num_groups)

        ### Step 6: Perform Local Backtracking, Phase 2 ###
        # Attempt to increase the number of preferred pairings and "additional" overlapping
        #   availability by swapping students between groups.
        self.__backtracking_phase_2()

        # Save and return the current solution as the best solution found
        self.best_solution_found = self.groups
        self.best_solution_found.sort(key=lambda x: int(x.group_id))
        self.best_solution_score = self.cur_sol_score

        # Clear any final print statement in preparation for it to be overwritten
        self.console_printer.print("")

        return self

    def __start_grouping(self, grouping_pass: int, num_groups: int):
        '''
        This method performs steps 1 thru 4 of the grouping algorithm.
        Step 1: Pre-process Student List
        Step 2: Construct Initial Groups
        Step 3: Perform Local Backtracking, Phase 1
        Step 4: Save the Current "Optimal" Solution
        '''
        for i in range(num_groups):
            self.groups.append(models.GroupRecord(f'{i+1}', []))

        ### Step 1: Pre-process Student List ###
        preprocessed_data: list[models.SurveyRecord] = self.__pre_process_students(
        )

        ### Step 2: Construct Initial Groups ###
        self.__construct_initial_groups(preprocessed_data, num_groups)

        ### Step 3: Perform Local Backtracking, Phase 1 ###
        self.__backtracking_phase_1(grouping_pass)

        ### Step 4: Save the Current "Optimal" Solution ###
        # Check if the current solution (groups) score better than the saved best solution
        if (grouping_pass == 0 or (self.cur_sol_score > self.best_solution_score) or
            ((self.cur_sol_score == self.best_solution_score)
                and (scoring.standard_dev_groups(self.groups, self.scoring_vars) < scoring.standard_dev_groups(self.best_solution_found, self.scoring_vars)))):
            self.best_solution_found = self.groups
            self.best_solution_score = self.cur_sol_score

    def __pre_process_students(self) -> list[models.SurveyRecord]:
        '''
        This method preprocesses the student list:
        The student list will be sorted based on number of dislikes, with those having
            the most dislikes at the top of the list. This should improve performance of
            the algorithm by forcing “difficult” students (those with a lot of dislikes) to
            be grouped first.
        Note: some randomization is included within this list by randomizing the order of
            students with the same number of dislikes. This means that each run can/should
            produce different results.
        '''
        # For each student’s disliked users list, remove duplicate entries
        for student in self.survey_data:
            student.disliked_students = [*set(student.disliked_students)]

        # Sort students from most disliked to least (not in place)
        # Also, for subsets of students with the same number of dislikes,
        #  randomly shuffle the subset
        sorted_students: list[models.SurveyRecord] = self.__sort_students_by_dislikes(
        )

        # Process "no survey students" per the configuration selection (no_survey_group_method)
        if self.config_data["no_survey_group_method"] != models.NoSurveyGroupMethodConsts.STANDARD_GROUPING:
            # Place "no survey students" at the top of the list
            sorted_students_copy = deepcopy(sorted_students)
            for student in sorted_students_copy:
                if not student.provided_survey_data:
                    # Remove the student from their current position in the list
                    sorted_students.remove(student)
                    # Add the student to the beginning (top) of the list
                    sorted_students.insert(0, student)

        # return the pre-processed student data
        return sorted_students

    def __sort_students_by_dislikes(self) -> list[models.SurveyRecord]:
        '''
        This private/helper method sorts students from most disliked to least (not in place)
        Also, for subsets of students with the same number of dislikes, the subset is randomly
            shuffled.
        '''
        num_dislikes: dict[str, int] = {}
        for student in self.survey_data:
            num_dislikes[student.student_id] = 0
        for student in self.survey_data:
            for disliked_student in student.disliked_students:
                if disliked_student in num_dislikes:
                    num_dislikes[disliked_student] = num_dislikes[disliked_student] + 1
        data_with_dislikes = zip(
            list(num_dislikes.values()), self.survey_data)
        lists_of_survey_records: list[list[models.SurveyRecord]] = [
            [] for _ in range(max(num_dislikes.values()) + 1)]
        for tuple_x in data_with_dislikes:
            lists_of_survey_records[tuple_x[0]].append(tuple_x[1])
        sorted_data: list[models.SurveyRecord] = []
        for list_x in lists_of_survey_records:
            if len(list_x) > 0:
                rnd.shuffle(list_x)
                for survey in list_x:
                    sorted_data.append(survey)

        # Put most disliked at the top of the list
        sorted_data.reverse()

        return sorted_data

    def __construct_initial_groups(self, preprocessed_data: list[models.SurveyRecord], num_groups: int):
        '''
        This function constructs/forms the initial groups by adding each student to a group one at a
            time from the "preprocessed" list generated in step 1 (top to bottom).
        When considering which group to add a student to, the disliked pairings and
                availability overlap constraints are considered, and an attempt at
                optimizing these results is made.
        '''
        # Determine if non-target groups are larger or smaller (or if N/A)
        # (0 = all standard, 1 = some larger, -1 = some smaller)
        non_stand_mod: int = self.__get_non_stand_mod(num_groups)

        # Determine number of groups with non-target size
        num_non_targ_groups: int = self.__get_num_non_targ_groups(
            non_stand_mod, num_groups)

        # Assign the first student to group 1
        self.groups[0].members.append(preprocessed_data[0])
        preprocessed_data.pop(0)

        # For each remaining student on the list (top to bottom), assign them to a group:
        count_groups_max_size: int = 0
        while len(preprocessed_data) > 0:
            student_assigned: bool = False
            student_survey: models.SurveyRecord = preprocessed_data[0]
            group_added_to: models.GroupRecord = models.GroupRecord(
                "invalid", [])

            # If the config selection for "no_survey_group_method" is "DISTRIBUTE_EVENLY",
            #  then we simply move through the groups in order until all "no survey students"
            #  have been assigned.
            if (self.config_data["no_survey_group_method"] == models.NoSurveyGroupMethodConsts.DISTRIBUTE_EVENLY and
                    not student_survey.provided_survey_data):
                group_added_to = self.groups[0]
                previous_group: models.GroupRecord = self.groups[0]
                for group in self.groups:
                    if previous_group.members > group.members:
                        # We've identified the "next" group
                        group_added_to = group
                        break

                # Add the student to the identified group
                group_added_to.members.append(student_survey)
                student_assigned = True

            if not student_assigned:
                # For each group, 1 to max group num:
                for group in self.groups:
                    # If the group is full, continue to the next group.
                    if self.__is_group_full(group, non_stand_mod, num_non_targ_groups, count_groups_max_size):
                        continue

                    # If the student increases the number of disliked pairings in the group, continue
                    #  to the next group.
                    if (True in validate.group_dislikes_user(student_survey.student_id, group).values() or
                            len(validate.user_dislikes_group(student_survey, group)) > 0):
                        continue

                    # If the group currently has availability overlap AND would not have availability
                    # overlap if this student were added, continue to the next group.
                    if (len(group.members) != 0 and validate.availability_overlap_count(group) > 0 and
                            not validate.fits_group_availability(student_survey, group)):
                        continue

                    # Else, assign the student to this group and break from the for loop.
                    group.members.append(student_survey)
                    group_added_to = group
                    student_assigned = True
                    break

            # If the student has not yet been assigned to a group, then assign them to the first
            #   potential group for which the total number of disliked pairings would be increased
            #  the least.
            if not student_assigned:
                # identify the index of the group that raises the number of dislikes the least
                least_dislike_increase_idx: int = self.__least_dislike_increase(
                    student_survey, non_stand_mod, num_non_targ_groups, count_groups_max_size)

                # Add the student to the identified group
                self.groups[least_dislike_increase_idx].members.append(
                    student_survey)
                group_added_to = self.groups[least_dislike_increase_idx]
                student_assigned = True

            # "pop" the student now that they have been assigned
            preprocessed_data.pop(0)

            # Increment count of groups at max size, if applicable
            if self.__group_at_max_size(group_added_to, non_stand_mod):
                count_groups_max_size += 1

    def __backtracking_phase_1(self, grouping_pass: int):
        '''
        This private/helper method performs the first local backtracking phase of the grouping alg:
            First, an attempt to eliminate disliked pairings is made by swapping students that are
                part of such pairings into other groups.
            Second, an attempt to eliminate groups without an overlapping time slot is made by
                swapping key students into other groups.
            NOTE: At each backtracking step, considered swaps are only performed if they
                are found to improve or at least not decrease the solution's score.
        '''
        # Calculate the current solution score
        self.scoring_vars = \
            models.GroupSetData("solution_1",
                                self.config_data["target_group_size"],

                                len((self.config_data["field_mappings"])[
                                    "preferred_students_field_names"]),

                                sum(len(group.members)
                                    for group in self.groups),

                                len((self.config_data["field_mappings"])[
                                    "availability_field_names"]),

                                validate.total_groups_no_availability(
                                    self.groups),

                                validate.total_disliked_pairings(self.groups),

                                validate.total_liked_pairings(self.groups),

                                sum(
                                    # subtract one to get "additional"
                                    max(validate.availability_overlap_count(
                                        group) - 1, 0)
                                    for group in self.groups))
        self.cur_sol_score = scoring.score_groups(self.scoring_vars)

        # Attempt to eliminate disliked pairings by swapping students that are part of such
        # pairings into other groups.
        self.__eliminate_dislikes(grouping_pass)

        # Attempt to eliminate groups without an overlapping time slot by swapping key students
        #   into other groups.
        self.__eliminate_missing_overlap(grouping_pass)

    def __eliminate_dislikes(self, grouping_pass: int):
        '''
        This private/helper method attempts to eliminate any disliked pairings by swapping students
            that are part of such pairings into other groups.
        '''
        loop_count: int = 0
        student_swapped: bool = True
        improvement_swap: bool = True
        no_improvement_count: int = 0

        # While there are more than 0 disliked pairings AND
        #   the iteration limit has not been met AND
        #   progress is being made (student_swapped and improvement):
        # Continue to attempt to find improvement swaps.
        while ((validate.total_disliked_pairings(self.groups) > 0) and
                (loop_count < max((self.config_data["grouping_passes"]*10), 100)) and
                (student_swapped and no_improvement_count < 10)):

            loop_count += 1
            self.console_printer.print("Loop " + str(grouping_pass + 1) +
                                       " Targetting Disliked Pairings " + str(loop_count))

            # increment the counter tracking the number of loops without improvement, as necessary
            if improvement_swap:
                no_improvement_count = 0
            else:
                # previous loop didn't produce an improvement
                no_improvement_count += 1

            # Reset boolean trackers
            student_swapped = False
            improvement_swap = False

            # Determine the group with the most dislike pairings.
            group_max_disliked_pairs: models.GroupRecord = self.__group_max_dislikes()

            # Shuffle the group to avoid getting stuck swapping the same student over and over
            rnd.shuffle(group_max_disliked_pairs.members)

            # For each student in other groups, if swapping the group_max_disliked_pairs student
            #   with this student would improve (lower) the overall solution score, swap the two
            #   students and break from the for loop.
            for idx_stud_most_dislike, _ in enumerate(group_max_disliked_pairs.members):

                if self.__attempt_swap(idx_stud_most_dislike, group_max_disliked_pairs, False):
                    student_swapped = True
                    improvement_swap = True
                    break

            # If no improvement swap was found, try swapping a group member from
            # group_max_disliked_pairs into another group to retain an equivalent score
            if not improvement_swap:
                # For each student in other groups, if swapping the group_max_disliked_pairs
                #   student with this student would retain an equivalent overall solution score,
                #   swap the two students and break from the for loop.
                for idx_stud_most_dislike, _ in enumerate(group_max_disliked_pairs.members):
                    if self.__attempt_swap(idx_stud_most_dislike, group_max_disliked_pairs, True):
                        student_swapped = True
                        break

    def __eliminate_missing_overlap(self, grouping_pass: int):
        '''
        This private/helper method attempts to eliminate any groups without an overlapping time
            slot by swapping key students into other groups.
        '''
        student_swapped = True
        improvement_swap = True
        no_improvement_count = 0
        loop_count = 0

        # While there are more than 0 groups without an overlapping timeslot AND
        #   the iteration limit has not been met AND
        #   progress is being made (student_swapped):
        # Continue to attempt to find improvement swaps.
        while ((validate.total_groups_no_availability(self.groups) > 0) and
                (loop_count < max((self.config_data["grouping_passes"]*10), 100)) and
                (student_swapped and no_improvement_count < 10)):

            loop_count += 1
            self.console_printer.print("Loop " + str(grouping_pass + 1) +
                                       " Targetting Overlap Improvement " + str(loop_count))
            improvement_swap: bool = False
            student_swapped = False

            # For each group without an overlapping timeslot:
            for group in self.groups:
                if validate.meets_group_availability_requirement(group):
                    continue

                # Deterimine if there is a single student preventing an overlapping
                # slot (stud_prev_overlap)
                idx_stud_prevent_overlap: int = validate.stud_prev_overlap_idx(
                    group)

                if idx_stud_prevent_overlap != -1:
                    # For each student in other groups, if swapping stud_prevent_overlap
                    #  with this student would improve (lower) the overall solution score,
                    #  swap the two students.
                    if self.__attempt_swap(idx_stud_prevent_overlap, group, False):
                        improvement_swap = True
                        student_swapped = True
                    # If no improvement swap was found, try to find an "equivalent" swap instead
                    elif self.__attempt_swap(idx_stud_prevent_overlap, group, True):
                        student_swapped = True
                # If no improment swap has been found:
                if not improvement_swap:
                    # choose a random student within the group (stud_rand_overlap):
                    idx_stud_rand_overlap: int = rnd.randint(
                        0, len(group.members) - 1)
                    # For each student in other groups, if swapping stud_rand_overlap
                    #  with this student would improve (lower) the overall solution score,
                    #  swap the two students.
                    if self.__attempt_swap(idx_stud_rand_overlap, group, False):
                        improvement_swap = True
                        student_swapped = True
                    # If no improvement swap was found, try to find an "equivalent" swap instead
                    elif self.__attempt_swap(idx_stud_rand_overlap, group, True):
                        student_swapped = True

            # increment the counter tracking the number of loops without improvement, as necessary
            if improvement_swap:
                no_improvement_count = 0
                continue
            # loop didn't produce an improvement
            no_improvement_count += 1

    def __backtracking_phase_2(self):
        '''
        This private/helper method performs the second backtracking phase of the grouping alg:
            Attempt to increase the number of preferred pairings and "additional" overlapping
                availability by swapping students between groups.
            NOTE: Considered swaps will only be performed if they are found to improve the
                solution's score.
        '''
        self.groups = self.best_solution_found
        self.cur_sol_score = self.best_solution_score
        loop_count = 0
        student_swapped = True

        # While the iteration limit has not been met AND
        #   progress is being made (student_swapped):
        # Continue to attempt to find improvement swaps.
        while (loop_count < max((self.config_data["grouping_passes"]*10), 100) and student_swapped):

            loop_count += 1
            self.console_printer.print("Preferred Pairings & Availability Improvement " +
                                       str(loop_count))

            student_swapped = False
            improvement_swap: bool = False

            # Shuffle the groups to avoid continually focusing on the same group
            rnd.shuffle(self.groups)

            # Determine the number of preferred pairings in each group
            pref_pairs_by_group: list[tuple] = []
            for idx, group in enumerate(self.groups):
                pref_pairs_by_group.append(
                    (idx, validate.total_liked_pairings([group])))

            # Focus on the groups with the least preferred pairs first
            pref_pairs_by_group.sort(key=lambda x: x[1])
            for group_tuple in pref_pairs_by_group:
                # For each student in the group, try swapping the student into another group
                # to improve the solution score
                group: models.GroupRecord = self.groups[group_tuple[0]]
                for idx, _ in enumerate(group.members):
                    # improvement swap attempt first
                    if self.__attempt_swap(idx, group, False):
                        student_swapped = True
                        improvement_swap = True
                if improvement_swap:
                    break

    def __attempt_swap(self, stud_idx_in_group: int, student_group: models.GroupRecord, equiv_swap_ok: bool) -> bool:
        '''
        This private/helper method attempts to swap the student identified by stud_idx_in_group in
        the student_group with students in the other groups in order to (depending on the value of
        equiv_swap_ok) improve or at least maintain the solution's score.
        '''

        student_provided_survey_data: bool = student_group.members[
            stud_idx_in_group].provided_survey_data

        for group in self.groups:
            if group == student_group:
                continue

            cur_sol_std_dev: float = 0
            if equiv_swap_ok:
                cur_sol_std_dev = scoring.standard_dev_groups(
                    self.groups, self.scoring_vars)

            # shuffle the group to avoid getting stuck swapping the same student over and over
            rnd.shuffle(group.members)
            for idx, student in enumerate(group.members):
                # NOTE: If the config selection for "no_survey_group_method" is DISTRIBUTE_EVENLY or
                #    GROUP_TOGETHER (i.e., not STANDARD_GROUPING), then swapping of students should
                #    only be attempted IF their "provided_survey_data" member variable matches.
                if student.provided_survey_data != student_provided_survey_data:
                    continue

                # swap the students
                group.members[idx] = student_group.members[stud_idx_in_group]
                student_group.members[stud_idx_in_group] = student

                # Get the new score
                self.scoring_vars.num_groups_no_overlap = validate.total_groups_no_availability(
                    self.groups)
                self.scoring_vars.num_disliked_pairs = validate.total_disliked_pairings(
                    self.groups)
                self.scoring_vars.num_preferred_pairs = validate.total_liked_pairings(
                    self.groups)

                new_sol_score: float = scoring.score_groups(
                    self.scoring_vars)
                if equiv_swap_ok:
                    if (new_sol_score > self.cur_sol_score or
                            (new_sol_score == self.cur_sol_score and
                             (cur_sol_std_dev >= scoring.standard_dev_groups(self.groups, self.scoring_vars)))):
                        self.cur_sol_score = new_sol_score
                        break
                else:
                    if ((new_sol_score > self.cur_sol_score) or
                            (new_sol_score == self.cur_sol_score and
                             (cur_sol_std_dev > scoring.standard_dev_groups(self.groups, self.scoring_vars)))):
                        self.cur_sol_score = new_sol_score
                        break

                # If we're here, the new solution was NOT better, so swap the students back
                student_group.members[stud_idx_in_group] = group.members[idx]
                group.members[idx] = student
            else:
                continue  # executed if the inner loop didn't break
            return True  # executed if the inner loop DID break. Successful swap
        return False  # no successful swap

    def __get_non_stand_mod(self, num_groups: int) -> int:
        '''
        This private/helper method determines if groups of non-target size are larger or smaller,
        or if N/A (0 = all standard/target, 1 = some larger, -1 = some smaller)
        '''
        result: int = 0
        if (num_groups * self.config_data["target_group_size"]) < len(self.survey_data):
            result = 1
        elif (num_groups * self.config_data["target_group_size"]) > len(self.survey_data):
            result = -1
        return result

    def __get_num_non_targ_groups(self, non_stand_mod: int, num_groups: int) -> int:
        '''
        This private/helper method determines the number of groups with non-target size.
        '''
        result: int = 0
        if non_stand_mod == 1:
            if ((len(self.survey_data) % (self.config_data["target_group_size"] + non_stand_mod) == 0) and
                    (len(self.survey_data) % num_groups == 0)):
                result = num_groups
            else:
                result = len(self.survey_data) % num_groups
        if non_stand_mod == -1:
            if ((len(self.survey_data) % (self.config_data["target_group_size"] + non_stand_mod) == 0) and
                    (len(self.survey_data) % num_groups == 0)):
                result = num_groups
            else:
                result = num_groups - (len(self.survey_data) % num_groups)
        return result

    def __is_group_full(self, group: models.GroupRecord, non_stand_mod: int, num_non_targ_groups: int, count_groups_max_size: int) -> bool:
        '''
        This private/helper method determines if a group is full based on:
            - the target group size
            - whether or not non-standard groups within this solution are
                intended to be larger or smaller than the target size
            - the overall number of groups
            - the number of groups already at the max size
        Returns true if determined to be full and false otherwise.
        '''
        larger_than_target: bool = (
            len(group.members) > self.config_data["target_group_size"])

        target_met_and_is_max: bool = (len(group.members) == self.config_data["target_group_size"] and (
            non_stand_mod <= 0 or (non_stand_mod == 1 and count_groups_max_size >= num_non_targ_groups)))

        lower_max_met: bool = (non_stand_mod == -1 and len(group.members) == (
            self.config_data["target_group_size"] - 1) and count_groups_max_size >= (self.num_groups - num_non_targ_groups))

        return larger_than_target or target_met_and_is_max or lower_max_met

    def __least_dislike_increase(self, student_survey: models.SurveyRecord, non_stand_mod: int, num_non_targ_groups: int, count_groups_max_size: int) -> int:
        '''
        This private/helper method determines what group the student (identified by
            'student_survey') should be added to in order to raise the number of disliked
            parings the least amount possible.
        Returns the index of the group identified.
        '''
        cur_total_dislikes: int = validate.total_disliked_pairings(
            self.groups)
        min_dislikes_increase: int = 0
        stored_group_idx: int = -1

        for idx, group in enumerate(self.groups):

            # If the group is full, continue to the next group.
            if self.__is_group_full(group, non_stand_mod, num_non_targ_groups, count_groups_max_size):
                continue

            group.members.append(student_survey)
            if stored_group_idx == -1:
                min_dislikes_increase = validate.total_disliked_pairings(
                    self.groups) - cur_total_dislikes
                stored_group_idx = idx
            else:
                dislikes_increase: int = validate.total_disliked_pairings(
                    self.groups) - cur_total_dislikes
                if dislikes_increase < min_dislikes_increase:
                    min_dislikes_increase = dislikes_increase
                    stored_group_idx = idx
            group.members.pop()
        return stored_group_idx

    def __group_at_max_size(self, group: models.GroupRecord, non_stand_mod: int) -> bool:
        '''
        The private/helper method determins if a group is at the maximum size based on:
            - the target group size
            - whether or not non-standard groups within this solution are
                intended to be larger or smaller than the target size
        '''
        return ((non_stand_mod == 1 and len(group.members) > self.config_data["target_group_size"]) or
                (non_stand_mod == -1 and len(group.members) >= self.config_data["target_group_size"]))

    def __group_max_dislikes(self) -> models.GroupRecord:
        '''
        This private/helper method identifies and returns a group containing the max number of
            disliked pairings within the group set.
        '''
        max_dislike_pairs: int = 0
        group_max_disliked_pairs: models.GroupRecord = self.groups[0]
        for group in self.groups:
            disliked_pairs: int = validate.total_disliked_pairings([
                group])
            if ((disliked_pairs > max_dislike_pairs) or
                    (disliked_pairs == max_dislike_pairs and bool(rnd.randint(0, 1)))):
                max_dislike_pairs = disliked_pairs
                group_max_disliked_pairs = group
        return group_max_disliked_pairs
