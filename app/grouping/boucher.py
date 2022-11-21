# pylint: disable="trailing-whitespace"
# pylint: disable="line-too-long
# These disables are temporary
'''
This is Branden Boucher's attempt at a grouping algorithm. 

First, a few terms.


Pass: refers to one execution of the entire grouping process
Run: refers to one execution of the grouping algorithm within a single pass. There will be multiple runs within a single pass
Passes: a list of all results of each execution of a pass
Runs: a list of all results from executions of the grouping algorithm
User: synonymous with survey record
Student: synonymous with User

Priorities:
Minimize disliked pairings (top priority)
At least one overlapping time slot (second priority)
Maximize preferred pairings (third priority)


This is a take on a Greedy randomized adaptive search procedure (GRASP).

The very first step of any pass will be the randomization of the order of the survey records. 
This will only take place once per pass
A tally of disliked users will be created where each user will be assigned the number of times they appear in other user’s disliked lists.
A separately ordered list will be created that will update the order of the users based on this tally with the highest number at the top of the list (descending order)
This will only take place once per pass
The number of groups and the number of users in each group will be calculated 
This will only take place once per pass
A grouping run will start. 
Each run will start with the user at the top of the list. 
After each run, the user at the top of the list will be moved to the bottom and all users will be marked as available
The number of runs will be the same as the number of users in the list
After all of the grouping runs and scoring are complete, a new pass will start.
The number of passes is dependent on the number specified in the config file

Grouping Run: Each Run starts with an index of 0, pointing to the user at the top of the list. Note: This algorithm attempts to get the most disliked users into groups first, where they are not disliked
	
The first available user at or after the current index of the list will be added to the current group. If this is the first time through, the current group will be the first group
Next, the first user in the list of dislike tallies that does not appear in the current group’s list of dislikes and is marked as available will be placed in the group.
This use will then marked as unavailable
If a user does not exist in the list of dislike tallies that is not in the list of dislikes for the group, the next user in the normal list that does not appear in the dislike tally list and is marked as available, will be added to the group and and marked as unavailable
If no user from either group is available, the next user in the normal list will be added to the group and marked as unavailable
Repeat starting at step 2 until the group is full
Once the group is full, a new group will be created. Then the process will start again at step 1
After all groups are filled the index will be incremented and the current run will be complete and scoring will take place. For scoring, the lower the score, the better. Note: this scoring is similar but different than that used for reporting.
Each group will receive a point for each dislike pairing in the group.
Additionally, the Run will receive a score. The score will increase by one point for each group that contains at least one dislike pair.
Each group will then receive points based on availability. The points added to the group’s score will be equal to the number of possible time slots minus the number of overlapping time slots. Overlapping time slots means that all users of the group have that time slot available. For example, if there are 10 available slots and the group shares 2 overlapping slots, then the group will receive 8 points.
Finally, each group will receive additional points equal to the number of users in their group minus the number of users that have at least one preferred pairing in the group. For instance, for a group of 5, if 3 people in the group have at least one preferred pairing with someone else in the group, the group will receive 2 points.
After all of the scoring is done for the groups in a run, a mean score for all groups and the max deviation from the mean will be calculated and recorded for the run.

The next run will start again at step 1 of the grouping run.

A pass is complete when all runs have been completed. The number of passes is determined by the specification in the config file.

After all passes have been completed, three runs will be selected from each pass: The first run with the lowest dislike score, the first run with the lowest mean score, and the first run with the lowest deviation score.

From each of the three, if one run is listed twice or three times, it will be automatically selected as the winner. If there are three distinct runs, The run with the lowest deviation will be selected first. If there is a tie for this, the lowest dislike will be considered next, and then finally the lowest mean score. If more than one pass was run, the same selection process will be applied to all winning runs selected from each pass.


'''
from dataclasses import dataclass
import random
from statistics import mean, stdev
from app import core, models


@dataclass
class AvailableUser:
    '''
    Data class for users with availability flag
    '''
    user: models.SurveyRecord
    is_used: bool = False


@dataclass
class DislikedUser:
    '''
    Data class for users with tally of dislikes and availability flag
    '''
    user: models.SurveyRecord
    dislikes: int = 0
    is_used: bool = False


@dataclass
class GroupScores:
    '''
    Data class for mean and deviation scores for all groups in a run
    '''
    mean: float
    deviation: float


@dataclass
class RunScores:
    '''
    Data class for the scores in a run
    '''
    run_score: int
    group_scores: GroupScores


@dataclass
class GroupingRun:
    '''
    Data class for an individual run
    '''
    groups: list[models.GroupRecord]
    scores: RunScores


@dataclass
class Pass:
    '''
    Data class for an individual pass
    '''
    runs: list[GroupingRun]

time_slots: int = 0

def create_groups(config: models.Configuration,
                  survey_data: list[models.SurveyRecord]) -> list[models.GroupRecord]:
    '''
    function for grouping students
    '''
    passes: list[Pass] = []
    groups: list[models.GroupRecord] = []
    group_sizes: list[int] = core.get_group_sizes(
        survey_data, config["target_group_size"])

    passes = __do_passes(config["grouping_passes"], survey_data, group_sizes)

    groups = __select_winners(passes, False)[0].groups
    time_slots = config["field_mappings"]["availability_field_names"]

    return groups


def __reset_availability(liked_users: list[AvailableUser], dislike_tallies: list[DislikedUser]):
    '''
    This method resets the avaiable bool flag on the lists of users
    '''

    for user in liked_users:
        user.is_used = False

    for user in dislike_tallies:
        user.is_used = False


def __radomize_users(survey_data: list[models.SurveyRecord]) -> list[models.SurveyRecord]:
    '''
    Randomizes the list of users
    Also adds a bool to indicate usage. True means used
    '''
    users: list[models.SurveyRecord] = []

    for record in survey_data:
        users.append(record)

    random.shuffle(users)

    return users


def by_tally(ele: DislikedUser):
    '''
    utility method for sorting dislike users by dislikes 
    '''
    return ele.dislikes


def __tally_dislikes(survey_data: list[models.SurveyRecord]) -> list[DislikedUser]:
    '''
    Creates a list of users that includes the number of dislikes they have
    Also adds a bool to indicate usage
    '''

    tallies: dict[str, DislikedUser] = {}

    # first create the tallies

    for record in survey_data:
        for user in record.disliked_students:

            # add the user if they don't exist
            if not user in tallies:
                record = __get_user_by_id(user, survey_data)
                if record is not None:
                    tally: DislikedUser = DislikedUser(record, 0, False)
                    tallies[user] = tally

            # increment the count
            tallies[user].dislikes += 1

    tally_values: list[DislikedUser] = []
    for value in tallies.items():
        tally_values.append(value[1])

     # finally, sort the list by the tallie count
    sorted(tally_values, key=by_tally, reverse=True)

    return tally_values

def __get_liked_users(rand_users: list[models.SurveyRecord], disliked_users: list[DislikedUser]) -> list[AvailableUser]:
    '''
    Returns a list of users that are not in the list of disliked users
    '''

    liked_users : list[AvailableUser] = []

    for user in rand_users:
        for disliked in disliked_users:
            if disliked.user.student_id == user.student_id:
                break
        else:
            liked_users.append(AvailableUser(user, False))

    return liked_users



def __get_user_by_id(user_id: str, survey_data: list[models.SurveyRecord]):
    '''
    Gets the SurveyRecord for a user based on the user id
    Returns null if not found
    '''

    for user in survey_data:
        if user_id == user.student_id:
            return user

    return None


def __do_passes(to_do: int, survey_data: list[models.SurveyRecord], group_sizes: list[int]) -> list[Pass]:
    '''
    Executes the number passes specified in the config
    '''

    passes: list[Pass] = []
    rand_users: list[models.SurveyRecord] = []
    dislike_tallies: list[DislikedUser] = []
    liked_users: list[AvailableUser] = []
    for pass_index in range(to_do):
        rand_users = __radomize_users(survey_data)
        dislike_tallies = __tally_dislikes(survey_data)
        liked_users = __get_liked_users(rand_users, dislike_tallies)
        passes.append(__do_runs(rand_users, liked_users, dislike_tallies, group_sizes))

    return passes


def __do_runs(rand_users: list[models.SurveyRecord], 
    liked_users: list[AvailableUser],
    dislike_tallies: list[DislikedUser], 
    group_sizes: list[int]) -> Pass:
    '''
    Executes all the runs in a pass
    '''
    runs: Pass = Pass([])

    for run_index in range(len(rand_users)):
        __reset_availability(liked_users, dislike_tallies)
        runs.runs.append(__execute_run(
            run_index, rand_users, liked_users, dislike_tallies, group_sizes))

    return runs


def __execute_run(starting_index: int, 
    rand_users: list[models.SurveyRecord], 
    liked_users: list[AvailableUser],
    dislike_tallies: list[DislikedUser], 
    group_sizes: list[int]) -> GroupingRun:
    '''
    This handles the grouping for all groups
    '''

    scores = RunScores(0, GroupScores(0, 0))
    run: GroupingRun = GroupingRun([], scores)

    for size in group_sizes:
        run.groups.append(__execute_grouping(
            size, starting_index, liked_users, dislike_tallies))

    scores.group_scores = __score_groups(run.groups)
    scores.run_score = __calc_run_score(run, rand_users)

    return run


def __execute_grouping(group_size: int, 
    starting_index: int, 
    liked_users: list[AvailableUser],
    dislike_tallies: list[DislikedUser]) -> models.GroupRecord:
    '''
    This does the actual grouping for a single group at a time
    '''
    group: models.GroupRecord = models.GroupRecord("", [])
    first_user: bool = True
    # if the group is not full get the first liked user

    while len(group.members) < group_size:

        user_index: int = -1
        # For the first user, try to get a liked user first
        if first_user:
            user_index = __get_next_user_index(starting_index, liked_users)

        # if no liked users are available get the first disliked who's not on a disliked list
        if user_index < 0:
            user_index = __get_next_disliked_user_index(
                dislike_tallies, group, False)

            # if not dislike user is available get first avilable disliked
            if user_index < 0:
                user_index = __get_next_disliked_user_index(
                    dislike_tallies, group, True)
                # if still no user is available try liked users again
                if user_index < 0 and not first_user:
                    first_user = True
                    continue
                
                # if we got here then we ran out of users too soon
                if user_index < 0:                
                    raise Exception(
                        "Ran out of users to group before all groups filled.")

            # if we make it here, we either have a disliked user to add or an exception
            group.members.append(dislike_tallies[user_index].user)
            dislike_tallies[user_index].is_used = True  # mark the user as used

        else:
            group.members.append(liked_users[user_index].user)
            liked_users[user_index].is_used = True  # mark the user as used

        first_user = False

    return group


def __get_next_user_index(starting_index: int, users: list[AvailableUser]) -> int:
    '''
    Gets the index of the next available user in the list 
    from a starting index then wraps around to the beginning
    If no users is found, -1 is returned
    '''
    actual_index: int = 0
    user_count: int = len(users)
    # we have to start at the starting index and loop around
    for index in range(0, len(users)):

        actual_index = index + starting_index
        if actual_index >= user_count:
            actual_index -= user_count
        # if user is not marked as used (a.ka. available)
        if not users[actual_index].is_used:
            return index

    # if we reach here, no available user was found
    return -1


def __get_next_disliked_user_index(diskiled_tallies: list[DislikedUser], 
    current_group: models.GroupRecord, 
    ignore_disliked_lists: bool) -> int:
    '''
    returns the index of the first available user from
    the dislike tallies list that does not appear in any
    user's dislike list of the current group
    If no users is found, -1 is returned
    '''
    for index, tally in enumerate(diskiled_tallies):
        # Now if the user in the dislikes is available and
        # the user is not in any dislike lists (or we are ignoring the dislike lists)
        if not tally.is_used and (ignore_disliked_lists or not __is_user_in_dislikes(tally.user, current_group)):
            return index

    return -1


def __is_user_in_dislikes(user: models.SurveyRecord, current_group: models.GroupRecord) -> bool:
    '''
    returns true if the user is in the dislikes list
    of anyone in the group
    '''

    for member in current_group.members:
        for disliked in member.disliked_students:
            if disliked == user.student_id:
                return True

    return False


def __score_groups(groups: list[models.GroupRecord]) -> GroupScores:
    '''
    Applies scoring to the groups in a run
    Scores are returned in the same order as the groups
    '''
    individual_scores: list[int] = []
    for group in groups:
        individual_scores.append(__calc_group_score(group))

    return GroupScores(mean(individual_scores), stdev(individual_scores))


def __calc_group_score(group: models.GroupRecord) -> int:
    '''
    Calculates the score for an individual group
    '''
    score: int = 0

    # Fisrt up is the dislike scoring
    score = __calc_dislike_group_score(group)
    score += __calc_availability_score(group)
    score += __calc_preferred_score(group)

    return score

def __calc_dislike_group_score(group: models.GroupRecord) -> int:
    '''
    Does the calculation of the dislikes for a group
    A point is gained for each dislike pair
    '''

    score: int = 0

    for user in group.members:
        for other_user in group.members:
            if other_user != user:
                for user_id in other_user.disliked_students:
                    if user.student_id == user_id:
                        score += 1

    return score


def __calc_availability_score(group: models.GroupRecord) -> int:
    '''
    Caclulates the availability score for a group
    Points start at number of available time slots
    and points are removed for each timeslot that
    all users share 
    '''

    score: int = time_slots
# TODO: Finish this scoring
    return score

def __calc_preferred_score(group: models.GroupRecord) -> int:
    '''
    Does the calculation of the preferred for a group
    Score starts at the number of users in the group and a
    point is subtracted for any user that has at least one
    preferred pair in the group
    '''

    score: int = len(group.members)

    for user in group.members:
        for other_user in group.members:
            if other_user != user:
                for user_id in other_user.preferred_students:
                    if user.student_id == user_id:
                        score -=1
                        break 
                else:
                    continue # this will continue if the inner break did not occurr
                break # this will break if the inner break oocurred

    return score

def __calc_run_score(run: GroupingRun, survey_data: list[models.SurveyRecord]) -> int:
    '''
    Calcualtes the score for an idividual run
    A point is added for each group that contains at least 
    one disliked pair
    '''
    score: int = 0

    for group in run.groups:
        for user in survey_data:
            if __is_user_in_dislikes(user, group):
                score += 1
                break

    return score


def __select_winners(passes: list[Pass], select_multiple_winners: bool) -> list[GroupingRun]:
    '''
    Selects the winner or winners, depending on config options
    '''
    winning_runs: list[GroupingRun] = []

    return winning_runs
