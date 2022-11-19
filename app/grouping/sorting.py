'''
This file contains a class that finds unique groups.
'''
from app import models

class UniqueGrouper:
    '''
    This class creates unique groups based on all the possible combinations for each student.
    '''
    def create_groups(self, survey_data: list, target_group_size: int, num_groups: int) -> list[models.GroupRecord]:
        '''
        This method finds all possible group combinations in the survey and removes any duplicates.
        '''
        return []
