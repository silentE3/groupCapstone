'''
validate is used for validating groups
'''
from app import models

WEEK_DAYS = [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'sunday'
]


def user_availability(user: models.SurveyRecord,
                      group: list[models.SurveyRecord]) -> dict[str, dict[str, bool]]:
    '''
    compares a users availability against a group and returns the resulting availability:
    ```
    {'time_slot': {'weekday': 'are_all_users_available(boolean)'}}
    ```
    '''
    user_available: dict[str, dict[str, bool]] = {}

    # create a map with each time and set to true for every day
    for key in user.availability.keys():
        user_available[key] = {}
        for day in WEEK_DAYS:
            if user.availability[key].count(day) > 0:
                user_available[key][day] = True
            else:
                user_available[key][day] = False

    # loop through the members and set to False if it isn't met
    for member in group:
        for key in member.availability.keys():
            for day in WEEK_DAYS:
                if member.availability[key].count(day) == 0:
                    user_available[key][day] = False

    return user_available


def user_matches_availability_count(user: models.SurveyRecord, group: list[models.SurveyRecord]):
    '''
    returns how many times the user is compatible with the group
    '''
    availability_count = 0
    user_available = user_availability(user, group)
    for vals in user_available.values():
        for available in vals.values():
            if available:
                availability_count += 1
    return availability_count


def fits_group_availability(user: models.SurveyRecord, group: list[models.SurveyRecord], min_count=1) -> bool:
    '''
    checks if the user meets the specified availability overlap count for the group
    '''
    return user_matches_availability_count(user, group) >= min_count


def group_availability(group: list[models.SurveyRecord]):
    '''
    Returns the availability of the group as a dictionary.
    Dictionary returned is the following structure:
    ```
    {'time_slot': {'weekday': are_available(boolean)}}
    ```
    The boolean value will be set to true if everyone that matches the given weekday in the timeslot
    '''
    group_available: dict[str, dict[str, bool]] = {}

    # create a map with each time and set to true for every day
    for key in group[0].availability.keys():
        group_available[key] = {}
        for day in WEEK_DAYS:
            group_available[key][day] = True

    # loop through the members and set to False if it isn't met
    for member in group:
        for key in member.availability.keys():
            for day in WEEK_DAYS:
                if member.availability[key].count(day) == 0:
                    group_available[key][day] = False
    return group_available


def availability_overlap_count(group: list[models.SurveyRecord]):
    '''
    gets the number of times that the group has overlap on their availability. i.e. how many timeslot-days everyone is available
    '''
    availability_count = 0
    group_available = group_availability(group)
    for vals in group_available.values():
        for available in vals.values():
            if available:
                availability_count += 1
    return availability_count


def meets_group_availability_requirement(group: list[models.SurveyRecord], min_count=1) -> bool:
    '''
    checks if the group meets the specified availability overlap count.
    '''
    return availability_overlap_count(group) >= min_count


def group_dislike_occurrences(group: list[models.SurveyRecord]) -> dict[str, list[str]]:
    '''
    returns the occurrences where there are disliked users in a group.
    goes through each user and returns a dict with the list of disliked users who occur in the group per user

    ```
    {'student_id': ['user_list']}
    ```
    '''

    disliked_occurrences: dict[str, list[str]] = {}

    for user in group:
        disliked_occurrences[user.student_id] = []
        for dislike_user in group:
            if dislike_user.student_id in user.disliked_students:
                disliked_occurrences[user.student_id].append(
                    dislike_user.student_id)

    return disliked_occurrences


def group_dislikes_user(user: str, group: list[models.SurveyRecord]) -> dict[str, bool]:
    '''
    checks whether the user id will fit for the users in the group. Returns a dictionary for each user in the group:
    ```
    {"student_id": "dislikes_student? (True/False)"}
    ```
    '''
    dislike_occurrences = {}

    for group_user in group:
        dislike_occurrences[group_user.student_id] = user in group_user.disliked_students

    return dislike_occurrences


def user_dislikes_group(user: models.SurveyRecord, group: list[models.SurveyRecord]) -> list[str]:
    '''
    returns each user in the group that matched with the disliked users
    '''
    disliked_users = []

    for group_user in group:
        if group_user.student_id in user.disliked_students:
            disliked_users.append(group_user.student_id)

    return disliked_users


def meets_group_dislike_requirement(user: models.SurveyRecord, group: list[models.SurveyRecord], max_dislike_count=0):
    '''
    checks if the user fits under the maximum dislike count threshold for the group
    '''

    group_dislike = group_dislikes_user(user.student_id, group)

    return len(user_dislikes_group(user, group)) + list(group_dislike.values()).count(True) <= max_dislike_count
