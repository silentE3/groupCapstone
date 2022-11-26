'''
validate is used for validating groups
'''
import re
import itertools
from app import models

WEEK_DAYS = [
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'sunday'
]


def user_availability(user: models.SurveyRecord, group: models.GroupRecord) -> dict[str, dict[str, bool]]:
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
    for member in group.members:
        for key in member.availability.keys():
            for day in WEEK_DAYS:
                if member.availability[key].count(day) == 0:
                    user_available[key][day] = False

    return user_available


def user_matches_availability_count(user: models.SurveyRecord, group: models.GroupRecord) -> int:
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


def fits_group_availability(user: models.SurveyRecord, group: models.GroupRecord, min_count=1) -> bool:
    '''
    checks if the user meets the specified availability overlap count for the group
    '''
    return user_matches_availability_count(user, group) >= min_count


def group_availability(group: models.GroupRecord) -> dict[str, dict[str, bool]]:
    '''
    Returns the availability of the group as a dictionary.
    Dictionary returned is the following structure:
    ```
    {'time_slot': {'weekday': are_available(boolean)}}
    ```
    The boolean value will be set to true if everyone that matches the given weekday in the timeslot
    '''
    group_available: dict[str, dict[str, bool]] = {}

    if len(group.members) == 0:
        return group_available

    # create a map with each time and set to true for every day
    for key in group.members[0].availability.keys():
        group_available[key] = {}
        for day in WEEK_DAYS:
            group_available[key][day] = True

    # loop through the members and set to False if it isn't met
    for member in group.members:
        for key in member.availability.keys():
            # convert values to lowercase for comparison
            lowercase_avail: list[str] = [x.lower()
                                          for x in member.availability[key]]
            for day in WEEK_DAYS:
                if (lowercase_avail).count(day.lower()) == 0:
                    group_available[key][day] = False
    return group_available


def group_availability_strings(group: models.GroupRecord) -> list[str]:
    '''
    Returns the overlapping availability of the group as a list of strings.
    List entries have the following structure:
    ```
    <weekday> @ <time slot>
    ```
    '''
    available_slots: list[str] = []
    group_availability_dict: dict[str, dict[str, bool]
                                  ] = group_availability(group)
    for time_slot, availability_days in group_availability_dict.items():
        for day, available in availability_days.items():
            if available:
                available_slots.append(
                    day + " @ " + _extract_time_(time_slot))
    return available_slots


def _extract_time_(time_slot_str: str) -> str:
    '''
    This function accepts a time slot header and attempts to extract the time portion
    from within it, under the assumption that the time is within two brackets.
    Ex:
        input string of: "Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]"
            would return "0:00 AM - 3:00 AM"
    If the enclosing bracket pattern is not found, it simply returns the original string.
    '''
    search = re.search(r'\[(.*?)\]', time_slot_str)
    if search is not None:
        result = search.group(1)
    else:
        result = time_slot_str

    return result


def availability_overlap_count(group: models.GroupRecord) -> int:
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


def meets_group_availability_requirement(group: models.GroupRecord, min_count=1) -> bool:
    '''
    checks if the group meets the specified availability overlap count.
    '''
    return availability_overlap_count(group) >= min_count


def group_dislike_occurrences(group: models.GroupRecord) -> dict[str, list[str]]:
    '''
    returns the occurrences where there are disliked users in a group.
    goes through each user and returns a dict with the list of disliked users who occur in the group per user

    ```
    {'student_id': ['user_list']}
    ```
    '''

    disliked_occurrences: dict[str, list[str]] = {}

    for user in group.members:
        disliked_occurrences[user.student_id] = []
        for dislike_user in group.members:
            if dislike_user.student_id in user.disliked_students:
                disliked_occurrences[user.student_id].append(
                    dislike_user.student_id)

    return disliked_occurrences


def group_dislikes_user(user: str, group: models.GroupRecord) -> dict[str, bool]:
    '''
    checks whether the user id will fit for the users in the group. Returns a dictionary for each user in the group:
    ```
    {"student_id": "dislikes_student? (True/False)"}
    ```
    '''
    dislike_occurrences = {}

    for group_user in group.members:
        dislike_occurrences[group_user.student_id] = user in group_user.disliked_students

    return dislike_occurrences


def user_dislikes_group(user: models.SurveyRecord, group: models.GroupRecord) -> list[str]:
    '''
    returns each member in the group that matched with the user's disliked students
    '''
    disliked_users = []

    for group_user in group.members:
        if group_user.student_id in user.disliked_students:
            disliked_users.append(group_user.student_id)

    return disliked_users


def meets_group_dislike_requirement(user: models.SurveyRecord, group: models.GroupRecord, max_dislike_count=0) -> bool:
    '''
    checks if the user fits under the maximum dislike count threshold for the group
    '''

    group_dislike = group_dislikes_user(user.student_id, group)

    return len(user_dislikes_group(user, group)) + list(group_dislike.values()).count(True) <= max_dislike_count


def users_disliked_in_group(group: models.GroupRecord) -> list[str]:
    '''
    loops through each user in the group and lists all of the disliked users
    '''
    disliked_users = []

    disliked_users = list(itertools.chain.from_iterable(
        group_dislike_occurrences(group).values()))

    return disliked_users


def meets_dislike_requirement(group: models.GroupRecord, max_dislike_count=0):
    '''
    checks if the group meets the dislike requirements
    '''
    return len(users_disliked_in_group(group)) <= max_dislike_count


def group_like_occurrences(group: models.GroupRecord) -> dict[str, list[str]]:
    '''
    returns the occurrences where there are liked users in a group.
    goes through each user and returns a dict with the list of liked users who occur in the group per user

    ```
    {'student_id': ['user_list']}
    ```
    '''

    liked_occurrences: dict[str, list[str]] = {}

    for user in group.members:
        liked_occurrences[user.student_id] = []
        for like_user in group.members:
            if like_user.student_id in user.preferred_students:
                liked_occurrences[user.student_id].append(
                    like_user.student_id)

    return liked_occurrences


def group_likes_user(user: str, group: models.GroupRecord) -> dict[str, bool]:
    '''
    checks whether the user id will fit for the users in the group. Returns a dictionary for each user in the group:
    ```
    {"student_id": "likes_student? (True/False)"}
    ```
    '''
    like_occurrences = {}

    for group_user in group.members:
        like_occurrences[group_user.student_id] = user in group_user.preferred_students

    return like_occurrences


def user_likes_group(user: models.SurveyRecord, group: models.GroupRecord) -> list[str]:
    '''
    returns each user in the group that matched with the liked users
    '''
    liked_users = []

    for group_user in group.members:
        if group_user.student_id in user.preferred_students:
            liked_users.append(group_user.student_id)

    return liked_users


def meets_group_like_requirement(user: models.SurveyRecord, group: models.GroupRecord, min_like_count=0) -> bool:
    '''
    checks if the user fits above the minimum like count threshold for the group
    '''

    group_like = group_likes_user(user.student_id, group)

    return len(user_likes_group(user, group)) + list(group_like.values()).count(True) >= min_like_count


def meets_like_requirement(group: models.GroupRecord, min_like_count=0):
    '''
    checks if the group meets the like requirements
    '''

    return len(list(itertools.chain.from_iterable(group_like_occurrences(group).values()))) >= min_like_count


def group_likes_count(group: models.GroupRecord):
    return len(list(itertools.chain.from_iterable(group_like_occurrences(group).values())))


def duplicate_user_in_group(group: models.GroupRecord) -> bool:
    '''
    This method checks to see if there are any duplicates in a group.
    This will return true if there are any duplicates. False otherwise.
    '''
    check = False
    state = 1
    copy_user = []
    for user in group.members:
        for user2 in group.members:
            if user.student_id == user2.student_id:
                if state == 1:
                    state -= 1
                else:
                    check = True
                    if copy_user.count(user.student_id) == 0:
                        copy_user.append(user.student_id)

        state = 1
    return check


def duplicate_user_in_dataset(groups: list[models.GroupRecord]) -> bool:
    '''
    This method checks to see if there are any duplicates in different groups.
    This will return true if there are any duplicates. False otherwise.
    '''
    check = False
    state = 1
    group_list = []
    copy_user = []
    for group in groups:
        for student in group.members:
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


def total_disliked_pairings(groups: list[models.GroupRecord]) -> int:
    '''
    This method returns the total number of disliked pairings in a set
    of groups.
    '''
    result: int = 0

    for group in groups:
        for user in group.members:
            result += len(user_dislikes_group(user, group))
    return result


def total_groups_no_availability(groups: list[models.GroupRecord]) -> int:
    '''
    This method returns the total number of groups without an overlapping time
    slot in a set of groups.
    '''
    result: int = 0

    for group in groups:
        if availability_overlap_count(group) == 0:
            result += 1
    return result


def total_liked_pairings(groups: list[models.GroupRecord]) -> int:
    '''
    This method returns the total number of liked pairings in a set
    of groups.
    '''
    result: int = 0

    for group in groups:
        for user in group.members:
            result += len(user_likes_group(user, group))
    return result


def verify_all_users_grouped(users: list[models.SurveyRecord], groupings: list[models.GroupRecord]) -> list[models.SurveyRecord]:
    '''
    Verifies that all users in the survey data have been grouped
    Returns a list of ungrouped users. If there are no ungrouped users
    then the list will be empty
    '''

    ungrouped = []
    is_grouped: bool
    for user in users:
        is_grouped = False
        for group in groupings:
            if user in group.members:
                is_grouped = True
                break
        if not is_grouped:
            ungrouped.append(user)

    return ungrouped


def generate_preferred_pairs_per_group(groupings: list[models.GroupRecord]) -> dict[str, list[tuple[str, str]]]:
    '''
    Generates pairs of preferred users for each group
    '''
    groups = {}

    # here we are saying, for each group, then for each user, does the user's preferred list match users in the group
    for group in groupings:
        pairs = []
        group_id: str = group.group_id
        groups[group_id] = pairs
        for user in group.members:
            for pref in user.preferred_students:
                if __contains_id(pref, group.members):
                    pair: tuple[str, str] = (user.student_id, pref)
                    pairs.append(pair)
        pairs.sort(key=lambda x: x[0])
    return groups


def generate_preferred_list_per_user(groupings: list[models.GroupRecord]) -> dict[str, list[str]]:
    '''
    This will create a list of the preferred users in a group per user
    '''
    users = {}

    # here we are saying, for each group, then for each user, does the user's preferred list match users in the group
    for group in groupings:
        for user in group.members:
            users[user.student_id] = []
            for pref in user.preferred_students:
                if __contains_id(pref, group.members):
                    users[user.student_id].append(pref)
    return users


def __contains_id(student_id: str, members: list[models.SurveyRecord]) -> bool:
    '''
    Specifically looks for a student in a list of survey records based on student id.
    Returns true immediately if a student is found.
    '''

    for member in members:
        if member.student_id.lower() == student_id.lower():
            return True
    return False
