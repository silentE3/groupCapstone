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


def meets_dislike_requirement(group: list[models.SurveyRecord], max_dislike_count=0):
    '''
    checks if the group meets the dislike requirements
    '''
    return len(group_dislike_occurrences(group).values()) <= max_dislike_count


def duplicate_user_in_group(group: list[models.SurveyRecord]) -> bool:
    '''
    This method checks to see if there are any duplicates in a group.
    This will return true if there are any duplicates. False otherwise.
    '''
    check = False
    state = 1
    copy_user = []
    for user in group:
        for user2 in group:
            if user.student_id == user2.student_id:
                if state == 1:
                    state -= 1
                else:
                    check = True
                    if copy_user.count(user.student_id) == 0:
                        copy_user.append(user.student_id)

        state = 1
    return check


def duplicate_user_in_dataset(groups: list[list[models.SurveyRecord]]) -> bool:
    '''
    This method checks to see if there are any duplicates in different groups.
    This will return true if there are any duplicates. False otherwise.
    '''
    check = False
    state = 1
    group_list = []
    copy_user = []
    for group in groups:
        for student in group:
            group_list.append(student)

    for user in group_list:
        for user2 in group_list:
            if user.student_id == user2.student_id:
                if state == 1:
                    state -= 1
                else:
                    check = True
                    if copy_user.count(user.student_id) == 0:
                        copy_user.append(user.student_id)
        state = 1
    return check


def size_limit_in_dataset(groups: list[models.GroupRecord], limit: int) -> bool:
    '''
    This method checks to see if all of the groups size fit in the limit of the given target +/- 1.
    This will return true if they fit. False otherwise.
    '''
    size = 0
    for group in groups:
        size = len(group.members)
        if size > limit + 1 or size < limit - 1:
            return False
    return True
