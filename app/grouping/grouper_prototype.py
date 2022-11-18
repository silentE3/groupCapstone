'''This class creates groups via constructive, heuristic approach with local backtracking.'''

import random as rnd
from app import models
from app.group import validate
from app.group import scoring


class Grouper:
    '''
    This class creates groups via constructive, heuristic approach with local backtracking.
    '''

    def create_groups(self,
                      survey_data: list[models.SurveyRecord],
                      config_data: models.Configuration,
                      num_groups: int) -> list[models.GroupRecord]:
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
            Step 3: Perform Local Backtracking
                Now that a solution group set exists (from step 2), the solution will attempt to be
                    improved upon through local backtracking.
                First, an attempt to reduce the number of disliked pairings will be made by
                    swapping students that are part of such pairings into other groups.
                Second, an attempt to reduce the number of groups without an overlapping time slot
                    will be made by swapping key students into other groups.
                Third, an attempt to increase the number of preferred pairings will be made by (you
                    guessed it) swapping students between groups.
                NOTE: At each backtracking step, considered swaps will only be performed if they
                    are found to improve or at least not decrease the solution's score.
            Step 4: Save the Current "Optimal" Solution
                Compare the score of the solution produced by Step 3 to that of any currently saved
                “optimal” solution (from previous Step 1-4 runs, if applicable) and save whichever
                has a higher score.
            Step 5: Repeat Steps 1-4 TBD number of times.
        '''
        groups: list[models.GroupRecord] = []
        for i in range(num_groups):
            groups.append(models.GroupRecord(f'{i+1}', []))

        ### Step 1: Pre-process Student List ###

        # For each student’s disliked users list, remove duplicate entries
        for student in survey_data:
            student.disliked_students = [*set(student.disliked_students)]

        # Sort students from most disliked to least
        num_dislikes: dict[str, int] = {}
        for student in survey_data:
            num_dislikes[student.student_id] = 0
        for student in survey_data:
            for disliked_student in student.disliked_students:
                if disliked_student in num_dislikes.keys():
                    num_dislikes[disliked_student] = num_dislikes[disliked_student] + 1

            # For subsets of students with the same number of dislikes, randomly shuffle the subset
        data_with_dislikes = zip(list(num_dislikes.values()), survey_data)
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

        '''
        print(num_dislikes)
        for x in survey_data:
            print(x.student_id)

        for x in preprocessed_data:
            print(x.student_id)
        '''

        ### Step 2: Begin Constructing Groups ###

        # Determine if non-target groups are larger or smaller (or if N/A)
        # (0 = all standard, 1 = some larger, -1 = some smaller)
        non_stand_mod: int = 0
        if (num_groups * config_data["target_group_size"]) < len(survey_data):
            non_stand_mod = 1
        elif (num_groups * config_data["target_group_size"]) > len(survey_data):
            non_stand_mod = -1

        # Determine number of groups with non-target size
        num_non_targ_groups: int = 0
        if non_stand_mod == 1:
            num_non_targ_groups = len(
                survey_data) % config_data["target_group_size"]
        if non_stand_mod == -1:
            num_non_targ_groups = config_data["target_group_size"] - \
                (len(survey_data) % config_data["target_group_size"])

        # Assign the first student to group 1
        groups[0].members.append(preprocessed_data[0])
        preprocessed_data.pop(0)

        # For each student on the list (top to bottom)
        count_groups_max_size: int = 0
        while len(preprocessed_data) > 0:
            student_assigned: bool = False
            student_survey: models.SurveyRecord = preprocessed_data[0]
            # For each group, 1 to max group num:
            for group in groups:
                # If the group is full, continue to the next group.
                if ((len(group.members) > config_data["target_group_size"]) or
                        (len(group.members) == config_data["target_group_size"] and
                         (non_stand_mod <= 0 or
                         (non_stand_mod == 1 and count_groups_max_size >= num_non_targ_groups))) or
                        (non_stand_mod == -1 and len(group.members) == (config_data["target_group_size"] - 1) and
                         count_groups_max_size >= (num_groups - num_non_targ_groups))):
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
                else:
                    # Else, assign the student to this group and break from the for loop.
                    group.members.append(student_survey)
                    preprocessed_data.pop(0)
                    student_assigned = True
                    break

            # If the student has not yet been assigned to a group, then assign them to the
            #  first potential group for which the total number of disliked pairings would be increased
            #  the least.
            if not student_assigned:
                cur_total_dislikes: int = validate.total_disliked_pairings(
                    groups)
                min_dislikes_increase: int = 0
                stored_group_idx: int = -1
                for idx, group in enumerate(groups):
                    if ((len(group.members) > config_data["target_group_size"]) or
                            (len(group.members) == config_data["target_group_size"] and
                             (non_stand_mod <= 0 or
                             (non_stand_mod == 1 and count_groups_max_size >= num_non_targ_groups))) or
                            (non_stand_mod == -1 and len(group.members) == (config_data["target_group_size"] - 1) and
                             count_groups_max_size >= (num_groups - num_non_targ_groups))):
                        continue

                    group.members.append(student_survey)
                    if stored_group_idx == -1:
                        min_dislikes_increase = validate.total_disliked_pairings(
                            groups) - cur_total_dislikes
                        stored_group_idx = idx
                    else:
                        dislikes_increase: int = validate.total_disliked_pairings(
                            groups) - cur_total_dislikes
                        if (dislikes_increase < min_dislikes_increase):
                            min_dislikes_increase = dislikes_increase
                            stored_group_idx = idx
                    group.members.pop()
                groups[stored_group_idx].members.append(student_survey)
                preprocessed_data.pop(0)

        ### Step 3: Perform Local Backtracking ###
        scoring_vars = models.GroupSetData("solution_1",
                                           validate.total_groups_no_availability(
                                               groups),
                                           validate.total_disliked_pairings(
                                               groups),
                                           validate.total_liked_pairings(
                                               groups),
                                           config_data["target_group_size"],
                                           len((config_data["field_mappings"])[
                                               "preferred_students_field_names"]),
                                           sum(len(group.members) for group in groups))
        cur_sol_score: float = scoring.score_groups(scoring_vars)
        loop_count: int = 0
        student_swapped: bool = True
        # While there are more than 0 disliked pairings AND less than 1,000* iterations
        #  of this loop have occurred AND progress is being made (student_swapped):
        while (validate.total_disliked_pairings(groups) > 0 and loop_count < 1000 and student_swapped):
            print(cur_sol_score)
            student_swapped = False
            # Determine the group with the most dislike pairings.
            max_dislike_pairs: int = 0
            group_max_disliked_pairs: models.GroupRecord = groups[0]
            for group in groups:
                disliked_pairs: int = validate.total_disliked_pairings([group])
                if (disliked_pairs > max_dislike_pairs or (disliked_pairs == max_dislike_pairs and bool(rnd.randint(0, 1)))):
                    max_dislike_pairs = disliked_pairs
                    group_max_disliked_pairs = group

            print(group_max_disliked_pairs.group_id)

            # For this group (group_max_disliked_pairs), try swapping a group memeber into
            #  another group to improve the score
            '''
            # identify a student that is part of the most disliked
            #  pairings within the group(stud_most_dislike).
            max_num_dislike: int = 0
            idx_stud_most_dislike: int = 0
            stud_most_dislike: models.SurveyRecord = group_max_disliked_pairs.members[
                idx_stud_most_dislike]
            for idx, student in enumerate(group_max_disliked_pairs.members):
                num_dislike: int = len(validate.user_dislikes_group(
                    student, group_max_disliked_pairs))
                if (num_dislike > max_num_dislike or (num_dislike == max_num_dislike and bool(rnd.randint(0, 1)))):
                    max_num_dislike = num_dislike
                    stud_most_dislike = student
                    idx_stud_most_dislike = idx
            print(stud_most_dislike.student_id)
            '''

            for idx_stud_most_dislike, stud_most_dislike in enumerate(group_max_disliked_pairs.members):
                # For each student in other groups, if swapping the group_max_disliked_pairs student with this student
                #  would improve (lower) the overall solution score, swap the two students and break
                #  from the for loop.
                for group in groups:
                    if group == group_max_disliked_pairs:
                        continue
                    # shuffle the group to avoid getting stuck swapping the same student over and over
                    rnd.shuffle(group.members)
                    for idx, student in enumerate(group.members):
                        # swap the students
                        group.members[idx] = stud_most_dislike
                        group_max_disliked_pairs.members[idx_stud_most_dislike] = student

                        # Get the new score
                        scoring_vars.num_groups_no_overlap = validate.total_groups_no_availability(
                            groups)
                        scoring_vars.num_of_disliked_pairs = validate.total_disliked_pairings(
                            groups)
                        scoring_vars.num_of_preferred_pairs = validate.total_liked_pairings(
                            groups)

                        new_sol_score: float = scoring.score_groups(
                            scoring_vars)
                        if new_sol_score < cur_sol_score:
                            cur_sol_score = new_sol_score
                            student_swapped = True
                            break

                        # If we're here, the new solution was NOT better swap the students back
                        group.members[idx] = student
                        group_max_disliked_pairs.members[idx_stud_most_dislike] = stud_most_dislike
                    else:
                        continue  # executed if the inner loop didn't break
                    break  # executed if the inner loop DID break
                else:
                    continue  # executed if the inner loop didn't break
                break  # executed if the inner loop DID break

            # If no improvement swap was found, try swapping a group member from
            # group_max_disliked_pairs into another group to retain an equivalent score
            for idx_stud_most_dislike, stud_most_dislike in enumerate(group_max_disliked_pairs.members):
                # For each student in other groups, if swapping the group_max_disliked_pairs student with this student
                #  would retain an equivalent overall solution score, swap the two students and break
                #  from the for loop.
                for group in groups:
                    if group == group_max_disliked_pairs:
                        continue
                    # shuffle the group to avoid getting stuck swapping the same student over and over
                    rnd.shuffle(group.members)
                    for idx, student in enumerate(group.members):
                        # swap the students
                        group.members[idx] = stud_most_dislike
                        group_max_disliked_pairs.members[idx_stud_most_dislike] = student

                        # Get the new score
                        scoring_vars.num_groups_no_overlap = validate.total_groups_no_availability(
                            groups)
                        scoring_vars.num_of_disliked_pairs = validate.total_disliked_pairings(
                            groups)
                        scoring_vars.num_of_preferred_pairs = validate.total_liked_pairings(
                            groups)

                        new_sol_score: float = scoring.score_groups(
                            scoring_vars)
                        if new_sol_score <= cur_sol_score:
                            cur_sol_score = new_sol_score
                            student_swapped = True
                            break

                        # If we're here, the new solution was NOT better swap the students back
                        group.members[idx] = student
                        group_max_disliked_pairs.members[idx_stud_most_dislike] = stud_most_dislike
                    else:
                        continue  # executed if the inner loop didn't break
                    break  # executed if the inner loop DID break
                else:
                    continue  # executed if the inner loop didn't break
                break  # executed if the inner loop DID break

            loop_count += 1

            print(cur_sol_score)
            print(validate.total_disliked_pairings(groups))

        # While there are more than 0 groups without an overlapping timeslot AND less than 1,000*
        #  iterations of this loop have occurred AND progress is being made (student_swapped):
        student_swapped = True
        loop_count = 0
        while (validate.total_disliked_pairings(groups) > 0 and loop_count < 1000 and student_swapped):
            # For each group without an overlapping timeslot:
            for group in groups:
                if validate.meets_group_availability_requirement(group):
                    continue
                # If there is a single student preventing an overlapping slot (stud_prev_overlap):
                stud_prevent_overlap: models.SurveyRecord
                student_found: bool = False
                for idx, student in enumerate(group.members):
                    test_group: models.GroupRecord = models.GroupRecord(
                        group.group_id, group.members.copy())
                    test_group.members.pop(idx)
                    if validate.meets_group_availability_requirement(test_group):
                        stud_prevent_overlap = student
                        student_found = True
                    break

        return groups
