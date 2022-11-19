'''
This file contains a class that finds unique groups.
'''
import itertools
from app import models

class UniqueGrouper:
    '''
    This class creates unique groups based on all the possible combinations for each student.
    '''
    def create_groups(self, survey_data: list, target_group_size: int, num_groups: int) -> list[models.GroupRecord]:
        '''
        This method finds all possible group combinations in the survey and removes any duplicates.
        '''
        # Determine if non-target groups are larger or smaller (or if N/A)
        # (0 = all standard, 1 = some larger, -1 = some smaller)
        non_stand_mod = 0
        if (num_groups * target_group_size) < len(survey_data):
            non_stand_mod = 1
        elif (num_groups * target_group_size) > len(survey_data):
            non_stand_mod = -1

        # Determine number of groups with non-target size
        num_non_targ_groups = 0
        if non_stand_mod == 1:
            num_non_targ_groups = len(survey_data) % target_group_size
        if non_stand_mod == -1:
            num_non_targ_groups = target_group_size - (len(survey_data) % target_group_size)

        groups: list[models.GroupRecord]
        groups = []

        #This part focuses on finding all possible group combinations
        combo1 = list(itertools.combinations(survey_data, target_group_size))
        #combo2 = list(itertools.combinations(survey_data, target_group_size + non_stand_mod))
        print(combo1)
        #print(combo2)

        return groups
