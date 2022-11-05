"""This will verify a list if grouping data and provide infomration
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
