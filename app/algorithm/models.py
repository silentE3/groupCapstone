from operator import contains
from app import generate


class User(object):
    """
    User holds information about a user
    """

    def __init__(self, asurite, available):
        self.asurite = asurite
        self.available = available


class Group():
    """
    Group holds information about a group 
    """

    def __init__(self, name) -> None:
        self.members: list[generate.UserRecord] = []
        self.name = name

    def meets_availability_requirement(self) -> bool:
        availability_met: dict[int, dict[str, bool]] = {}
        days = [
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'sunday'
        ]

        # create a map with each time and set to true for every day
        for key in self.members[0].days_available_by_time.keys():
            for day in days:
                availability_met[key] = {}
                availability_met[key][day] = True

        # loop through the members and set to False if it isn't met
        for member in self.members:
            for key in member.days_available_by_time.keys():
                for day in days:
                    if member.days_available_by_time[key].count(day) == 0:
                        availability_met[key][day] = False

        # now look and see if there is a day that works for everyone
        for vals in availability_met.values():
            for available in vals.values():
                if available:
                    return True

        return False

    def is_user_compatible(self, user_to_add: generate.UserRecord, user_to_remove_idx: int) -> bool:
        members_hypothetical = self.members.copy()
        members_hypothetical.pop(user_to_remove_idx)
        members_hypothetical.append(user_to_add)
        # if meets_dislike_requirement(members_hypothetical):
        #     return False
        availability_met: dict[int, dict[str, bool]] = {}
        days = [
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'sunday'
        ]

        # create a map with each time and set to true for every day
        for key in members_hypothetical[0].days_available_by_time.keys():
            for day in days:
                availability_met[key] = {}
                availability_met[key][day] = True

        # loop through the members and set to False if it isn't met
        for member in members_hypothetical:
            for key in member.days_available_by_time.keys():
                for day in days:
                    if member.days_available_by_time[key].count(day) == 0:
                        availability_met[key][day] = False

        # now look and see if there is a day that works for everyone
        for vals in availability_met.values():
            for available in vals.values():
                if available:
                    return True

        return False


def meets_dislike_requirement(members: list[generate.UserRecord]) -> bool:
    for member in members:
        for mem in members:
            if contains(mem.disliked_students, member.disliked_students):
                return False
    return True
