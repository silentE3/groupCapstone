'''This class creates groups via constructive, heuristic approach with local backtracking.'''

import random as rnd
from app import models
from app.group import validate


class Grouper:
    '''
    This class creates groups via constructive, heuristic approach with local backtracking.
    '''

    def create_groups(self,
                      survey_data: list[models.SurveyRecord],
                      target_group_size: int,
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

        print(num_dislikes)
        for x in survey_data:
            print(x.student_id)

        for x in preprocessed_data:
            print(x.student_id)

        ### Step 2: Begin Constructing Groups ###

        # Determine if non-target groups are larger or smaller (or if N/A)
        # (0 = all standard, 1 = some larger, -1 = some smaller)
        non_stand_mod: int = 0
        if (num_groups * target_group_size) < len(survey_data):
            non_stand_mod = 1
        elif (num_groups * target_group_size) > len(survey_data):
            non_stand_mod = -1

        # Determine number of groups with non-target size
        num_non_targ_groups: int = 0
        if non_stand_mod == 1:
            num_non_targ_groups = len(survey_data) % target_group_size
        if non_stand_mod == -1:
            num_non_targ_groups = target_group_size - \
                (len(survey_data) % target_group_size)

        # Assign the first student to group 1
        groups[0].members.append(preprocessed_data[0])
        preprocessed_data.pop(0)

        # For each student on the list (top to bottom)
        count_groups_max_size: int = 0
        while len(preprocessed_data) > 0:
            student_survey: models.SurveyRecord = preprocessed_data[0]
            # For each group, 1 to max group num:
            for group in groups:

                # If the group is full, continue to the next group.
                if ((len(group.members) > target_group_size) or
                        (len(group.members) == target_group_size and
                         (non_stand_mod <= 0 or
                         (non_stand_mod == 1 and count_groups_max_size >= num_non_targ_groups))) or
                        (non_stand_mod == -1 and len(group.members) == (target_group_size - 1) and
                         count_groups_max_size >= (num_groups - num_non_targ_groups))):
                    continue

                # If the student increases the number of disliked pairings in the group, continue
                #  to the next group.
                if (validate.group_dislikes_user(student_survey.student_id, group) or
                        validate.user_dislikes_group(student_survey, group)):
                    continue

                # If the group currently has availability overlap AND would not have availability
                # overlap if this student were added, continue to the next group.
                if (validate.availability_overlap_count(group) > 0 and
                        not validate.fits_group_availability(student_survey, group)):
                    continue
                else:
                    # Else, assign the student to this group and break from the for loop.
                    group.members.append(student_survey)
                    preprocessed_data.pop(0)

                # If the student has not yet been assigned to a group, then assign them to the
                #  first group for which the total number of disliked pairings would be increased
                #  the least.
                cur_total_dislikes: int = validate.total_disliked_pairings(
                    groups)
                min_dislikes_increase: int = 0
                stored_group_idx: int = -1
                for idx, group in enumerate(groups):
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
        return []
