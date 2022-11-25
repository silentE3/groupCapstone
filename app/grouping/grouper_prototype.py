'''This file contains the Grouper class, which creates groups via a constructive, heuristic approach with local backtracking.'''

import random as rnd
from app import models
from app.group import validate
from app.group import scoring


class Grouper:
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

    def __init__(self, survey_data, config_data, num_groups):
        self.survey_data = survey_data
        self.config_data = config_data
        self.groups = []
        self.best_solution_found = []
        self.best_solution_score = -1
        self.num_groups = num_groups

    def create_groups(self) -> list[models.GroupRecord]:
        '''
        function for grouping students via constructive, heuristic approach with local
            backtracking, as follows:

            Step 1: Pre-process Student List
                The student list will be sorted based on number of dislikes, with those having
                    the most dislikes at the top of the list. This should improve performance of
                    the algorithm by forcing “difficult” students (those with a lot of dislikes) to
                    be grouped first.
                Note: some randomization is included within this list by randomizing the order of
                    students with the same number of dislikes. This means that each run can/should
                    produce different results.
            Step 2: Construct Groups
                Groups will be formed by adding each student to a group one at a time from the list
                    generated in step 1 (top to bottom).
                When considering which group to add a student to, the disliked pairings and
                    availability overlap constraints will be considered, and an attempt at
                    optimizing these results will be made.
            Step 3: Perform Local Backtracking, Phase 1
                Now that a solution group set exists (from step 2), the solution will attempt to be
                    improved upon through local backtracking.
                First, an attempt to reduce the number of disliked pairings will be made by
                    swapping students that are part of such pairings into other groups.
                Second, an attempt to reduce the number of groups without an overlapping time slot
                    will be made by swapping key students into other groups.
                NOTE: At each backtracking step, considered swaps will only be performed if they
                    are found to improve or at least not decrease the solution's score.
            Step 4: Save the Current "Optimal" Solution
                Compare the score of the solution produced by Step 3 to that of any currently saved
                “optimal” solution (from previous Step 1-4 runs, if applicable) and save whichever
                has a higher score.
            Step 5: Repeat Steps 1-4 "grouping_passes" number of times (specified in the config)
            Step 6: Perform Local Backtracking, Phase 2
                An attempt to increase the number of preferred pairings will be made by
                    swapping students between groups.
                NOTE: Considered swaps will only be performed if they
                    are found to improve or at least not decrease the solution's score.
        '''

        # "Step 5": Repeat Steps 1-4 "grouping_passes" number of times (specified in the config)
        for grouping_pass in range(max(self.config_data["grouping_passes"], 1)):
            self.groups = []
            self.__start_grouping(grouping_pass, self.num_groups)

        ### Step 6: Perform Local Backtracking, Phase 2 ###
        self.groups = self.best_solution_found
        self.cur_sol_score = self.best_solution_score
        loop_count = 0
        student_swapped = True
        while (loop_count < max((self.config_data["grouping_passes"]*10), 100) and student_swapped):
            loop_count += 1
            print("Preferred Pairings Improvement " + str(loop_count))

            student_swapped = False
            improvement_swap: bool = False
            # avoid continually focusing on the same group
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
                    if self.attempt_swap(idx, group, False):
                        student_swapped = True
                        improvement_swap = True
                if improvement_swap:
                    break

            # print(self.cur_sol_score)

        self.best_solution_found = self.groups
        self.best_solution_found.sort(key=lambda x: int(x.group_id))
        self.best_solution_score = self.cur_sol_score

        return self.best_solution_found

    def attempt_swap(self, stud_idx_in_group: int, student_group: models.GroupRecord, equiv_swap_ok: bool) -> bool:
        '''
        This function attempts to swap the student identified by stud_idx_in_group in the
        student_group with students in the other groups in order to (depending on the value of
        equiv_swap_ok) improve or at least maintain the solution's score.
        '''
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
                        # print(group.members[idx].student_id + ", " + student_group.members[stud_idx_in_group].student_id)
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

    def __start_grouping(self, grouping_pass: int, num_groups: int):
        '''
        TODO: Placeholder
        '''
        for i in range(num_groups):
            self.groups.append(models.GroupRecord(f'{i+1}', []))

        ### Step 1: Pre-process Student List ###
        preprocessed_data: list[models.SurveyRecord] = self.__pre_process_students(
        )

        ### Step 2: Begin Constructing Groups ###
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
        # print(self.best_solution_score)

    def __pre_process_students(self) -> list[models.SurveyRecord]:
        '''
        TODO: Placeholder
        '''
        # For each student’s disliked users list, remove duplicate entries
        for student in self.survey_data:
            student.disliked_students = [*set(student.disliked_students)]

        # Sort students from most disliked to least
        num_dislikes: dict[str, int] = {}
        for student in self.survey_data:
            num_dislikes[student.student_id] = 0
        for student in self.survey_data:
            for disliked_student in student.disliked_students:
                if disliked_student in num_dislikes:
                    num_dislikes[disliked_student] = num_dislikes[disliked_student] + 1

        # For subsets of students with the same number of dislikes, randomly shuffle the subset
        data_with_dislikes = zip(
            list(num_dislikes.values()), self.survey_data)
        lists_of_survey_records: list[list[models.SurveyRecord]] = [
            [] for _ in range(max(num_dislikes.values()) + 1)]
        for tuple_x in data_with_dislikes:
            lists_of_survey_records[tuple_x[0]].append(tuple_x[1])

        preprocessed_data: list[models.SurveyRecord] = []
        for list_x in lists_of_survey_records:
            if len(list_x) > 0:
                rnd.shuffle(list_x)
                for survey in list_x:
                    preprocessed_data.append(survey)
        preprocessed_data.reverse()  # most disliked at top
        return preprocessed_data

    def __construct_initial_groups(self, preprocessed_data: list[models.SurveyRecord], num_groups: int):
        '''
        TODO: Placeholder
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

        # For each student on the list (top to bottom)
        count_groups_max_size: int = 0
        while len(preprocessed_data) > 0:
            student_assigned: bool = False
            student_survey: models.SurveyRecord = preprocessed_data[0]
            # For each group, 1 to max group num:
            for group in self.groups:
                # If the group is full, continue to the next group.
                larger_than_target: bool = (
                    len(group.members) > self.config_data["target_group_size"])
                target_met_and_is_max: bool = (len(group.members) == self.config_data["target_group_size"] and
                                               (non_stand_mod <= 0 or
                                                (non_stand_mod == 1 and count_groups_max_size >= num_non_targ_groups)))
                lower_max_met: bool = (non_stand_mod == -1 and len(group.members) == (self.config_data["target_group_size"] - 1) and
                                       count_groups_max_size >= (num_groups - num_non_targ_groups))
                if larger_than_target or target_met_and_is_max or lower_max_met:
                    continue

                # If the student increases the number of disliked pairings in the group, continue
                #  to the next group.
                if (validate.group_dislikes_user(student_survey.student_id, group) or
                        validate.user_dislikes_group(student_survey, group)):
                    continue

                # If the group currently has availability overlap AND would not have availability
                # overlap if this student were added, continue to the next group.
                if (len(group.members) != 0 and validate.availability_overlap_count(group) > 0 and
                        not validate.fits_group_availability(student_survey, group)):
                    continue

                # Else, assign the student to this group and break from the for loop.
                group.members.append(student_survey)
                preprocessed_data.pop(0)
                student_assigned = True

                # increment count of groups at max size if applicable
                if ((non_stand_mod == 1 and len(group.members) > self.config_data["target_group_size"]) or
                        (non_stand_mod == -1 and len(group.members) >= self.config_data["target_group_size"])):
                    count_groups_max_size += 1
                break

            # If the student has not yet been assigned to a group, then assign them to the
            #  first potential group for which the total number of disliked pairings would be increased
            #  the least.
            if not student_assigned:
                cur_total_dislikes: int = validate.total_disliked_pairings(
                    self.groups)
                min_dislikes_increase: int = 0
                stored_group_idx: int = -1
                for idx, group in enumerate(self.groups):
                    if ((len(group.members) > self.config_data["target_group_size"]) or
                            (len(group.members) == self.config_data["target_group_size"] and
                                (non_stand_mod <= 0 or
                                 (non_stand_mod == 1 and count_groups_max_size >= num_non_targ_groups))) or
                            (non_stand_mod == -1 and len(group.members) == (self.config_data["target_group_size"] - 1) and
                                count_groups_max_size >= (num_groups - num_non_targ_groups))):
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
                self.groups[stored_group_idx].members.append(
                    student_survey)

                # increment count of groups at max size if applicable
                if ((non_stand_mod == 1 and len(self.groups[stored_group_idx].members) > self.config_data["target_group_size"]) or
                        (non_stand_mod == -1 and len(self.groups[stored_group_idx].members) >= self.config_data["target_group_size"])):
                    count_groups_max_size += 1

                preprocessed_data.pop(0)

    def __backtracking_phase_1(self, grouping_pass: int):
        self.scoring_vars = models.GroupSetData("solution_1",
                                                self.config_data["target_group_size"],
                                                len((self.config_data["field_mappings"])[
                                                    "preferred_students_field_names"]),
                                                sum(len(group.members)
                                                    for group in self.groups),
                                                len((self.config_data["field_mappings"])[
                                                    "availability_field_names"]),
                                                validate.total_groups_no_availability(
                                                    self.groups),
                                                validate.total_disliked_pairings(
                                                    self.groups),
                                                validate.total_liked_pairings(
                                                    self.groups),
                                                sum(
                                                    # subtract one to get "additional"
                                                    max(validate.availability_overlap_count(
                                                        group) - 1, 0)
                                                    for group in self.groups))
        self.cur_sol_score = scoring.score_groups(self.scoring_vars)

        loop_count: int = 0
        student_swapped: bool = True
        improvement_swap: bool = True
        no_improvement_count: int = 0
        # While there are more than 0 disliked pairings AND the iteration limit has
        #  not been met AND progress is being made (student_swapped and improvement):
        while ((validate.total_disliked_pairings(self.groups) > 0) and
                (loop_count < max((self.config_data["grouping_passes"]*10), 100)) and
                (student_swapped and no_improvement_count < 10)):
            loop_count += 1
            print("Loop " + str(grouping_pass + 1) +
                  " Disliked Pairings Improvement " + str(loop_count))

            if improvement_swap:
                no_improvement_count = 0
            else:
                # previous loop didn't produce an improvement
                no_improvement_count += 1

            # print(self.cur_sol_score)
            student_swapped = False
            improvement_swap = False
            # Determine the group with the most dislike pairings.
            max_dislike_pairs: int = 0
            group_max_disliked_pairs: models.GroupRecord = self.groups[0]
            for group in self.groups:
                disliked_pairs: int = validate.total_disliked_pairings([
                    group])
                if ((disliked_pairs > max_dislike_pairs) or
                        (disliked_pairs == max_dislike_pairs and bool(rnd.randint(0, 1)))):
                    max_dislike_pairs = disliked_pairs
                    group_max_disliked_pairs = group

            # For this group (group_max_disliked_pairs), try swapping a group memeber into
            #  another group to improve the score
            # shuffle the group to avoid getting stuck swapping the same student over and over
            rnd.shuffle(group_max_disliked_pairs.members)
            for idx_stud_most_dislike, _ in enumerate(group_max_disliked_pairs.members):
                # For each student in other groups, if swapping the group_max_disliked_pairs student with this student
                #  would improve (lower) the overall solution score, swap the two students and break
                #  from the for loop.
                if self.attempt_swap(idx_stud_most_dislike, group_max_disliked_pairs, False):
                    student_swapped = True
                    improvement_swap = True
                    break

            # If no improvement swap was found, try swapping a group member from
            # group_max_disliked_pairs into another group to retain an equivalent score
            if not improvement_swap:
                for idx_stud_most_dislike, _ in enumerate(group_max_disliked_pairs.members):
                    # For each student in other groups, if swapping the group_max_disliked_pairs student with this student
                    #  would retain an equivalent overall solution score, swap the two students and break
                    #  from the for loop.
                    if self.attempt_swap(idx_stud_most_dislike, group_max_disliked_pairs, True):
                        student_swapped = True
                        break

            # print(self.cur_sol_score)
            # print(validate.total_disliked_pairings(self.groups))

        # While there are more than 0 groups without an overlapping timeslot AND the iteration
        #  limit has not been met AND progress is being made (student_swapped):
        student_swapped = True
        improvement_swap = True
        no_improvement_count = 0
        loop_count = 0
        while ((validate.total_groups_no_availability(self.groups) > 0) and
                (loop_count < max((self.config_data["grouping_passes"]*10), 100)) and
                (student_swapped and no_improvement_count < 10)):
            loop_count += 1
            print("Loop " + str(grouping_pass + 1) +
                  " Availability Improvement " + str(loop_count))

            if improvement_swap:
                no_improvement_count = 0
            else:
                # previous loop didn't produce an improvement
                no_improvement_count += 1

            improvement_swap: bool = False
            student_swapped = False
            # For each group without an overlapping timeslot:
            for group in self.groups:
                if validate.meets_group_availability_requirement(group):
                    continue
                # If there is a single student preventing an overlapping slot (stud_prev_overlap):
                idx_stud_prevent_overlap: int = -1
                for idx, _ in enumerate(group.members):
                    test_group: models.GroupRecord = models.GroupRecord(
                        group.group_id, group.members.copy())
                    test_group.members.pop(idx)
                    if validate.meets_group_availability_requirement(test_group):
                        idx_stud_prevent_overlap = idx
                    break
                if idx_stud_prevent_overlap != -1:
                    # For each student in other groups, if swapping stud_prevent_overlap
                    #  with this student would improve (lower) the overall solution score,
                    #  swap the two students.
                    if self.attempt_swap(idx_stud_prevent_overlap, group, False):
                        improvement_swap = True
                        student_swapped = True
                    # If no improvement swap was found, try to find an "equivalent" swap instead
                    else:
                        if self.attempt_swap(idx_stud_prevent_overlap, group, True):
                            student_swapped = True
                # If no improment swap has been found,
                # choose a random student within the group (stud_rand_overlap):
                if not improvement_swap:
                    idx_stud_rand_overlap: int = rnd.randint(
                        0, len(group.members) - 1)
                    # For each student in other groups, if swapping stud_rand_overlap
                    #  with this student would improve (lower) the overall solution score,
                    #  swap the two students.
                    if self.attempt_swap(idx_stud_rand_overlap, group, False):
                        improvement_swap = True
                        student_swapped = True
                    # If no improvement swap was found, try to find an "equivalent" swap instead
                    else:
                        if self.attempt_swap(idx_stud_rand_overlap, group, True):
                            student_swapped = True

            # print(str(self.cur_sol_score))
            # print(validate.total_groups_no_availability(self.groups))

    def __get_non_stand_mod(self, num_groups: int) -> int:
        result: int = 0
        if (num_groups * self.config_data["target_group_size"]) < len(self.survey_data):
            result = 1
        elif (num_groups * self.config_data["target_group_size"]) > len(self.survey_data):
            result = -1
        return result

    def __get_num_non_targ_groups(self, non_stand_mod: int, num_groups: int) -> int:
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
