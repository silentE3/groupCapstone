'''
This file includes functions to score entire group sets as well as
 individual groups, based on certain criteria.
'''
from math import trunc, sqrt
from app import models
from app.group import validate


def score_groups(variables: models.GroupSetData) -> float:
    '''
    This function scores a group set (entire grouping solution) based on:
        - number of disliked pairings
        - number of groups without an overlapping time slot
        - number of preferred/liked pairings

    Additionally, the scores are computed relative to a few fixed values within the solution
     set. These are:
        - number of students
        - max number of groups possible
        - number of preferred student slots on the student survey

    The scoring equation used is as follows:
        T (s, d, p ) = C1 + C2 * s + C3 * d – 0.1 * p
                s = number of groups without an overlapping time slot.
                d = number of disliked pairings.
                p = number of preferred/liked pairings

            C1, C2, C3 are considered constants for each solution set:
                C1 = (0.1 * N * P)
                C2 = C1 + 1
                C3 = C2 * G + C1 + 1

                Where,
                    N = the total number of students being grouped
                    P = number of preferred/liked student slots on the survey
                    G = max number of groups possible (based on the target group size +/- 1)

        NOTE: This equation guarantees the following about a solution (groupings), relative to
         other solutions within the solution set:
            - The solution with greater disliked pairings will always have the worse (higher) score
            - A solution with the same number of disliked pairings as another, but fewer groups
                with an overlapping time slot, will always have a worse (higher) score.
            - A solution with the same number of disliked pairings AND groups with an overlapping
                time slot as another, but more preferred pairings will always score better (lower).

    '''
    total_score: float = 0
    constant_1: float = 0.1 * variables.num_of_students * \
        variables.num_of_preferred_slots
    constant_2: float = constant_1 + 1

    max_num_groups_pos: int  # based on target group size
    if variables.target_group_size <= 1:
        # divide by 0 and invalid target group size protection
        variables.target_group_size = 1
        max_num_groups_pos = trunc(
            variables.num_of_students / variables.target_group_size)
    else:
        max_num_groups_pos = trunc(
            variables.num_of_students / (variables.target_group_size - 1))
    constant_3: float = constant_2 * max_num_groups_pos + constant_1 + 1

    total_score = constant_1 + (constant_2 * variables.num_groups_no_overlap) + (
        constant_3 * variables.num_of_disliked_pairs) - (0.1 * variables.num_of_preferred_pairs)
    return round(total_score, 2)


def score_individual_group(group: models.GroupRecord, variables: models.GroupSetData) -> float:
    '''
    This function scores an individual group using the T (s, d, p ) equation in the score_groups
     function, but with s, d, and p being specific to the group (i.e., s is 0 or 1 for the group,
     d is number of disliked pairings within the group, etc.).

    '''
    variables.num_of_disliked_pairs = validate.total_disliked_pairings([group])
    variables.num_of_preferred_pairs = validate.total_liked_pairings([group])
    variables.num_groups_no_overlap = \
        validate.total_groups_no_availability([group])
    return score_groups(variables)


def standard_dev_groups(groups: list[models.GroupRecord], variables: models.GroupSetData) -> float:
    '''
    This function computes the standard deviation of the individual group scores within
    a Group Set.

    '''
    if len(groups) == 0:
        return 0  # divide by 0 protection

    mean_groups: float = 0
    group_scores: list[float] = []
    for group in groups:
        score = score_individual_group(group, variables)
        mean_groups += score
        group_scores.append(score)
    mean_groups = mean_groups / len(groups)

    std_dev: float = sqrt(
        (sum((score-mean_groups)**2 for score in group_scores)) / len(group_scores))

    return std_dev
