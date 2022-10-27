"""
algorithm contains the logic to implement sorting algorithm
"""

from app.algorithm import models


class Alg:

    def __init__(self) -> None:
        self.groups: list[models.Group] = []
        self.users: list[models.User] = []
        self.max_group_count = 0

    def group_user(self, user: int) -> bool:
        """
        contains the logic to add a user to a group.
        This involves checking that certain criteria is met. First it looks to see if there are any open groups
        If there are groups, it then loops through each to check if they meet the criteria.
        If criteria are met, the user should be added to the group
        """
        # if group exists, check if it meets criteria.
        # If it does, check that there is room in group. Add them to group if there is room
        # If not room, see if there is another group available
        # if no groups meet criteria, check if there are any available
        # if nothing meets criteria, and the max number of groups are assigned,
        # swap the user with one that works.
        # swap_user groups the user

        # first fill each group.
        # now what do you do when the groups are all populated, and the person doesn't fit in any of the groups you specified?
        # you search for a group and set your current user to the one that you took over
        # now find a group for that user. call group_user(user) and do the same thing until you

        # If user is out of bounds, return
        if user >= len(self.users) - 1:
            return

        added_to_group = False
        for group in self.groups:
            if len(group.members) <= 4 and group.meets_criteria(
                    self.users[user]):
                group.members.append(self.users[user])
                added_to_group = True
                self.group_user(user + 1)
                return

        # made it past finding a group to add to, but still didn't get added
        if not added_to_group:
            for group in self.groups:
                if group.meets_criteria(self.users[user]):
                    group.members.append(self.users[user])
                    self.group_user(group.members.pop())
                    return

    def groups_full(self) -> bool:
        full_groups = 0
        for group in self.groups:
            if len(group.members) > 3:
                full_groups += 1
        return full_groups == len(self.groups)


def group_users(user_list: list[models.User]):
    """
    Groups users in the list provided.
    This loops through each of the users and calls group_user
    """
    alg = Alg()
    alg.groups = []
    alg.users = user_list
    alg.max_group_count = len(alg.users) // 4
    alg.group_user(0)


# find_group(user):
#   loop through the groups and assign a user to thegroup

# def swap_user(user: int, group: int) -> int:
#     # find the next group that would work for this user
#     # increment the swap count
#     for group in groups:
#         if group.meets_criteria(user):
#             member = group.members.pop()
#             group.members.append(users[user])


if __name__ == '__main__':
    group_users([
        models.User('a', 1),
        models.User('b', 1),
        models.User('c', 2),
        models.User('d', 1),
        models.User('e', 2),
        models.User('f', 1),
        models.User('g', 2)
    ])
