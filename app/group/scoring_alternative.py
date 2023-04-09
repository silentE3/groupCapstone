'''
This file includes functions to score entire group sets as well as
 individual groups, based on certain criteria.

 NOTE: This file follows the alternative (non-standard) scoring design,
    where each student having at least one preferred pairing is prioritized
    above all groups having at least one overlapping time slot.
'''

from app import models
from app.group.validate import max_num_groups_possible_scoring


#   Since we are so far along in our development, and have extensively used the existing
#   scoring algorithm (scoring.py) with success, I wanted to keep the new scoring algorithm
#   essentially separate from that one. Additionally, although they are quite similar,
#   there are some significant terminology differences that would make discussing them within the
#   same file confusing.


def score_groups(variables: models.GroupSetData) -> float:
    '''
    Scores a group set (entire grouping solution) and returns the score value as a float,
        where a HIGHER score indicates a better solution.

    The grouping solution is scored based on (in priority order):
        - number of disliked pairings
        - number of students that could (theoretically) have a preferred pair but do not
        - number of groups without an overlapping time slot
        - number of "additional" overlapping timeslots and preferred/liked pairings 
            NOTE: "Additional" meaning beyond the 1 required by a previous constraint.

    Also, the scores are computed relative to a few fixed values within the solution
     set. These are:
        - number of students
        - max number of groups possible (based on +/- 1 of the target group size)
        - number of preferred student slots on the student survey
        - number of time slots on the student survey

    The scoring equation used is as follows:
        S (g,a,s,d) = (0.1 * (G - g)) + (C4 * a) – (C2 * s) – (C3 * d)
                g = number of groups without at least one overlapping time slot
                a = # of additional preferred pairings and additional overlapping time slots  (combined)
                s = number of students that could possibly be but are not grouped with at least one of their “preferred” students
                d = number of disliked pairings

            C1, C2, C3, C4 are considered constants for each solution set:
                C1 = (0.1 * G)
                C2 = C1 + 1
                C3 = C2 * N + C1 + 1
                C4 = 0.1/(N * P + G * T)

                Where, 
                    N = the total number of students being grouped
                    P = number of preferred/liked student slots on the student survey
                    G = max number of groups possible (based on the target group size +/- 1)
                    T = number of time slots on the student survey

        NOTE: This equation guarantees the following about a solution (groupings), relative to
         other solutions within the solution set:
            - A solution with greater disliked pairings will always have the worse (lower) score.
            - A solution with the same number of disliked pairings as another, but fewer students
              with a preferred pairing, will always have a worse (lower) score.
            - A solution with the same number of disliked pairings AND students with a preferred
              pairing as another, but more groups with an overlapping time slot will always score
              better (higher) than the other.
            - A solution with the same number of disliked pairings AND students with a preferred pairing
               AND groups with an overlapping time slot, but more (combined) additional overlapping time
               slots/additional preferred pairings will always score better (higher).



    '''
    total_score: float = 0

    max_num_groups_pos: int = max_num_groups_possible_scoring(
        variables.target_group_size, variables.num_students)

    constant_1: float = 0.1 * max_num_groups_pos
    constant_2: float = constant_1 + 1

    constant_3: float = constant_2 * variables.num_students + constant_1 + 1
    constant_4: float = 0.1/(variables.num_students * variables.num_survey_preferred_slots + max_num_groups_pos *
                             variables.num_survey_time_slots)

    total_score = ((0.1 * (max_num_groups_pos - variables.num_groups_no_overlap)) +
                   (constant_4 * (variables.num_additional_overlap + variables.num_additional_pref_pairs)) -
                   (constant_2 * variables.num_students_no_pref_pairs) -
                   (constant_3 * variables.num_disliked_pairs))

    return round(total_score, 4)
