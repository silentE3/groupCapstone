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
        for entry in survey:
            survey_students.append(entry.student_name)
        
        #At this point, the survey_student list should have every student name from the survey data.
        #Next, we will check if all the students have answered the survey.

        missing_students = []
        for student in roster:
            if survey_students.count(student) == 0:
                missing_students.append(student)
