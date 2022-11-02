"""This will read in the grouping data from a CSV file and parse it.
The first line of the dataset data is assumed to be header data."""

from app import models

class GroupingDataReader:
    '''
    Reads in grouping data from a CSV and stores it in a data structure.
    '''

    def load(self, groupfile: str) -> list[models.GroupRecord]:
        '''
        Reads in grouping data into a list of GroupRecord objects
        '''
        print(groupfile)
        groups = []
        return groups
