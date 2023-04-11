'''
This file includes functions to score entire group sets as well as
 individual groups, based on certain criteria.

 NOTE: This file follows the initial (original/standard) scoring design,
    where all groups having at least one overlapping time slot is
    prioritized above each student having at least one preferred pairing.
'''
from math import sqrt
from app import models
from app.group import validate
from app.group import scoring_alternative


def score_groups(variables: models.GroupSetData) -> float:
    '''
    Scores a group set (entire grouping solution) and returns the score value as a float,
        where a HIGHER score indicates a better solution.

    The grouping solution is scored based on (in priority order):
        - number of disliked pairings
        - number of groups without an overlapping time slot
        - number of preferred/liked pairings
        - number of "additional" overlapping timeslots
            NOTE: "Additional" meaning beyond the one overlapping slot "required" per group.

    Additionally, the scores are computed relative to a few fixed values within the solution
     set. These are:
        - number of students
        - max number of groups possible
        - number of preferred student slots on the student survey
        - number of time slots on the student survey

    The scoring equation used is as follows:
        S (p, t, s, d ) = (0.1 * p) + (C4 * t) – (C2 * s) – (C3 * d)
                p = number of preferred/liked pairings
                t = number of additional overlapping time slots
                s = number of groups without an overlapping time slot
                d = number of disliked pairings

            C1, C2, C3, and C4 are considered constants for each solution set:
                C1 = (0.1 * N * P)
                C2 = C1 + 1
                C3 = C2 * G + C1 + 1
                C4 = 0.1/(G * T)

                Where,
                    N = the total number of students being grouped
                    P = number of preferred/liked student slots on the student survey
                    G = max number of groups possible (based on the target group size - 1)
                    T = number of time slots on the student survey

        NOTE: This equation guarantees the following about a solution (groupings), relative to
         other solutions within the solution set:
            - A solution with greater disliked pairings will always have the worse (lower) score.
            - A solution with the same number of disliked pairings as another, but fewer groups
                with an overlapping time slot, will always have a worse (lower) score.
            - A solution with the same number of disliked pairings AND groups with an overlapping
                time slot as another, but more preferred pairings will always score better (higher)
            - A solution with the same number of disliked pairings AND groups with an overlapping
                time slot AND preferred pairings as another, but more “additional overlapping time
                slots” will always score better (higher).
    '''
    total_score: float = 0

    constant_1: float = 0.1 * variables.num_students * \
        variables.num_survey_preferred_slots
    constant_2: float = constant_1 + 1

    max_num_groups_pos: int = validate.max_num_groups_possible_scoring(
        variables.target_group_size, variables.num_students)

    constant_3: float = constant_2 * max_num_groups_pos + constant_1 + 1
    constant_4: float = 0.1/(max_num_groups_pos *
                             variables.num_survey_time_slots)

    total_score = ((0.1 * variables.num_preferred_pairs) +
                   (constant_4 * variables.num_additional_overlap) -
                   (constant_2 * variables.num_groups_no_overlap) -
                   (constant_3 * variables.num_disliked_pairs))

    return round(total_score, 4)


def score_individual_group(group: models.GroupRecord, variables: models.GroupSetData, use_alternative_scoring: bool = False) -> float:
    '''
    This function scores an individual group using the overall scoring equation in the score_groups
     function, but with the input values being specific to the group.

    '''
    variables.num_disliked_pairs = validate.total_disliked_pairings([group])
    variables.num_preferred_pairs = validate.total_liked_pairings([group])
    variables.num_groups_no_overlap = \
        validate.total_groups_no_availability([group])
    variables.num_additional_overlap = max(validate.availability_overlap_count(
        group) - 1, 0)  # subtract one to get "additional"

    if use_alternative_scoring:
        variables.num_students_no_pref_pairs = 0  # ensure it starts at 0
        num_students_pref_pair_not_possible: int = 0
        for student in group.members:
            if student.pref_pairing_possible and len(validate.user_likes_group(student, group)) == 0:
                variables.num_students_no_pref_pairs += 1
            elif not student.pref_pairing_possible:
                num_students_pref_pair_not_possible += 1
        variables.num_additional_pref_pairs = variables.num_preferred_pairs - \
            (len(group.members) - variables.num_students_no_pref_pairs -
             num_students_pref_pair_not_possible)
        return scoring_alternative.score_groups(variables)
    # "else"
    return score_groups(variables)


def standard_dev_groups(groups: list[models.GroupRecord], variables: models.GroupSetData, use_alternative_scoring: bool = False) -> float:
    '''
    This function computes the standard deviation of the individual group scores within
    a Group Set.

    '''
    if len(groups) == 0:
        return 0  # divide by 0 protection

    mean_groups: float = 0
    group_scores: list[float] = []
    for group in groups:
        score = score_individual_group(
            group, variables, use_alternative_scoring)
        mean_groups += score
        group_scores.append(score)
    mean_groups = mean_groups / len(groups)

    std_dev: float = sqrt(
        (sum((score-mean_groups)**2 for score in group_scores)) / len(group_scores))

    return std_dev
