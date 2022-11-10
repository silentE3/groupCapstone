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
