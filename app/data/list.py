'''
This file will be in charge of adding missing students to the list.
'''
from app import models
from app.data import load

def add_missing_students(survey: list[models.SurveyRecord], roster: list[str]) -> list[models.SurveyRecord]:
    '''
    This method involves reading the survey data and adding any missing students from the student list
    to the survey data. This will be based on student id.
    '''
    new_survey_data = survey
    survey_students = []
    for entry in survey:
        survey_students.append(entry.student_id)

    #At this point, the survey_student list should have every student name from the survey data.
    #Next, we will check if all the students have answered the survey.

    missing_students = []
    for student in roster:
        if survey_students.count(student) == 0:
            missing_students.append(student)

    #At this point, all missing students should be in the missing students list.
    for asurite in missing_students:
        record = models.SurveyRecord (
            student_id=asurite
        )
        #This code will use the function that adds availiability to all time slots.
        record.availability = load.set_wildcard_availability(record)
        new_survey_data.append(record)

    return new_survey_data
