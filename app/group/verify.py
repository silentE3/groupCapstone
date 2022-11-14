"""This will verify a list if grouping data and provide informatation
on the validity of each group. This tally data will then be output to a file.
Some validation will be based off of the config file."""

from app import models


class VerifyGrouping():
    '''
    verify grouping data and output to a file
    '''

    def __init__(self, configuration: models.Configuration) -> None:
        self.config = configuration

    def __contains_id(self, student_id: str, members: list[models.SurveyRecord]) -> bool:
        '''
        Specifically looks for a student in a list of survey records based on student id.
        Returns true immediately if a student is found.
        '''

        for member in members:
            if member.student_id.lower() == student_id.lower():
                return True
        return False

    def verify(self, original_data:  list[models.SurveyRecord], groupings: list[models.GroupRecord], tally_file: str):
        '''
        Verifies a list of grouping data and outputs the results to a file
        '''

    def verify_all_users_grouped(self, users: list[models.SurveyRecord], groupings: list[models.GroupRecord]) -> list[models.SurveyRecord]:
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

    def generate_preferred_pairs_per_group(self, groupings: list[models.GroupRecord]) -> dict[str, list[tuple[str, str]]]:
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
                    if self.__contains_id(pref, group.members):
                        pair: tuple[str, str] = (user.student_id, pref)
                        pairs.append(pair)
            pairs.sort(key=lambda x: x[0])
        return groups

    def generate_preferred_list_per_user(self, groupings: list[models.GroupRecord]) -> dict[str, list[str]]:
        '''
        This will create a list of the preferred users in a group per user
        '''
        users = {}

        # here we are saying, for each group, then for each user, does the user's preferred list match users in the group
        for group in groupings:
            for user in group.members:
                users[user.student_id] = []
                for pref in user.preferred_students:
                    if self.__contains_id(pref, group.members):
                        users[user.student_id].append(pref)
        return users
