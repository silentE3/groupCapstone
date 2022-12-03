'''
This file contains a class that finds unique groups.
'''
from itertools import combinations
from app import models

class UniqueGrouper:
    '''
    This class creates unique groups based on all the possible combinations for each student.
    '''
    def create_groups(self, survey_data: list[models.SurveyRecord], target_group_size: int, num_groups: int) -> list[models.GroupRecord]:
        '''
        This method finds all possible group combinations in the survey and removes any duplicates.
        This method will not be considered due to it's stubborn approach to the problem.
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

        print("Number of groups: " + str(num_groups))
        print("Target group size: " + str(target_group_size))
        print("Number of non target groups: " + str(num_non_targ_groups))
        groups: list[models.GroupRecord]
        groups = []

        students: list[str]
        students = []

        #This part first gets the student id of every student and prints it out in terminal.
        for entry in survey_data:
            students.append(entry.student_id)
        
        print(students)
        
        groups2 = list(combinations(students, target_group_size))
        print(len(groups2))

            



        return groups
