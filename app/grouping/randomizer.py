'''This class creates groups by random assignment'''

import random as rnd
from app import models


class RandomGrouper:
    '''
    This class creates groups by random assignment
    '''

    def create_groups(self,
                      survey_data: list,
                      target_group_size: int,
                      num_groups: int) -> list[models.GroupRecord]:
        '''
        function for grouping students randomly
        '''
        # Randomly shuffle the data in preparation for random grouping
        rnd.shuffle(survey_data)

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
            num_non_targ_groups = target_group_size - \
                (len(survey_data) % target_group_size)

        # result: list[list[models.SurveyRecord]]
        result: list[models.GroupRecord]
        result = []
        survey_num = 0  # counter for which student we're assigning currently
        for i in range(0, num_groups):
            # result.append([])  # create the group
            members = list()

            group_size = target_group_size
            if i >= (num_groups - num_non_targ_groups):
                # Groups with non-target size
                group_size += non_stand_mod
            for _ in range(0, group_size):
                # result[i].append(survey_data[survey_num])
                members.append(survey_data[survey_num])
                survey_num += 1
            group = models.GroupRecord(f'Group #{i+1}', members)
            result.append(group)

        return result
