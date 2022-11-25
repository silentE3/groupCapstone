'''
This file will be in charge of adding missing students to the list.
'''
from app import models

class StudentList:
    '''
    This class provides a reader to the survey data and student list.
    '''
    def addStudents(self, survey: list[models.SurveyRecord], roster: list[str]):
        '''
        This method involves reading the survey data and adding any missing students from the student list
        to the survey data.
        '''
        survey_students = []