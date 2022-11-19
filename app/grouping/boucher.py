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
import random as rnd
from app import models




def create_groups(config: models.Configuration,
                  survey_data: list[models.SurveyRecord]) -> list[models.GroupRecord]:
    '''
    function for grouping students
    '''

    groups: list[models.GroupRecord] = []
    return groups

def __radomize_users(survey_data: list[models.SurveyRecord]) -> list[tuple[models.SurveyRecord, bool]]:
    '''
    Randomizes the list of users
    Also adds a bool to indicate usage
    '''
    users: list[tuple[models.SurveyRecord, bool]] = []

    return users


def __tally_dislikes(survey_data: list[models.SurveyRecord]) -> list[tuple[models.SurveyRecord, int, bool]]:
    '''
    Creates a list of users that includes the number of dislikes they have
    Also adds a bool to indicate usage
    '''

    tally: list[tuple[models.SurveyRecord, int, bool]] = []
    return tally

def __do_passes(to_do: int):
    '''
    Executes the number passes specified in the config
    '''
    pass_counts: int = 0
    passes: list = []

def __do_runs():
    '''
    Executes all the runs in a pass
    '''
    run_index: int = 0
    runs: list = []


def __score_groups():
    '''
    Applies scoring to the groups in a run
    '''

def __score_runs():
    '''
    Applies scoring to the runs in a pass
    '''

def __select_winners():
    '''
    Selects the winner or winners, depending on config options
    '''

def __execute_run():
    '''
    This handles the grouping for all groups
    '''

def __execute_grouping():
    '''
    This does the actual grouping for a single group at a time
    '''