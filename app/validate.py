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
