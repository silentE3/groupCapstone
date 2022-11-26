"""
Provides the ability to load data into the program including raw survey data and grouped data
"""

import csv
import datetime as dt
from app import models
from app.group import validate


def parse_asurite(val: str) -> str:
    '''
    parses a student's id from the string.
    Returns the first value when splitting a str on a space character
    '''
    return val.strip().split(" ", 1)[0]


def total_availability_matches(student: models.SurveyRecord, students: list[models.SurveyRecord]) -> int:
    """
    checks the student's availability against everyone elses and counts the number of times that they match
    Args:
        student (models.SurveyRecord): student to check matches for
        students (list[models.SurveyRecord]): full list of students
    Returns:
        int: number of times the student matches availability in the dataset
    """

    totals = 0

    for other_student in students:
        if student.student_id == other_student.student_id:
            continue

        for time, avail_days in other_student.availability.items():
            for avail_day in avail_days:
                if avail_day in student.availability[time] and not avail_day == '':
                    totals += 1

    return totals


def set_wildcard_availability(student: models.SurveyRecord):
    '''
    sets the availability to all days/times
    '''
    avail = {}
    for key in student.availability:
        avail[key] = validate.WEEK_DAYS

    return avail


def has_availability(student: models.SurveyRecord):
    '''
    checks if the student marked any days that they were available during the allotted time
    '''
    avail = 0
    for days in student.availability.values():
        avail += len(days)

    return avail > 0


def __preprocess_survey_data(students: list[models.SurveyRecord]):
    '''
    performs some basic "preprocessing" of the survey data to ensure the grouping algorithm can function expected.
    This includes the following:
    - checking for students that didn't add availability
    - checking for students that have availability that didn't match to anyone else's
    - checking for students that have preferred students that in turn disliked them (Not yet implemented)
    - checking for students that have preferred students that didn't match in their availability (Not yet implemented)
    '''
    for student in students:
        if not student.provided_availability:
            print(
                f"student '{student.student_id}' did not provide any availability")
            set_wildcard_availability(student)
        if total_availability_matches(student, students) == 0:
            print(
                f"student '{student.student_id}' did not have matching availability with anyone else")
            student.has_matching_availability = False


def __parse_survey_record(config, row) -> models.SurveyRecord:
    '''
    parses a survey record from a row in the dataset
    '''
    survey = models.SurveyRecord(row[config['student_id_field_name']])

    for field in config['preferred_students_field_names']:
        if row[field] != "":
            survey.preferred_students.append(
                parse_asurite(row[field]).lower())
    survey.preferred_students = list(set(survey.preferred_students))

    for field in config['disliked_students_field_names']:
        if row[field] != "":
            survey.disliked_students.append(
                parse_asurite(row[field]).lower())
    survey.disliked_students = list(set(survey.disliked_students))

    for field in config['availability_field_names']:
        survey.availability[field] = row[field].lower().split(';')

    if config.get('timezone_field_name'):
        survey.timezone = row[config['timezone_field_name']]
    if (config.get("student_name_field_name") and row[config["student_name_field_name"]]):
        survey.student_name = row[config["student_name_field_name"]]
    if (config.get("student_email_field_name") and row[config["student_email_field_name"]]):
        survey.student_email = row[config["student_email_field_name"]]
    if (config.get("student_login_field_name") and row[config["student_login_field_name"]]):
        survey.student_login = row[config["student_login_field_name"]]
    if (config.get("submission_timestamp_field_name") and row[config["submission_timestamp_field_name"]]):
        survey.submission_date = dt.datetime.strptime(
            row[config["submission_timestamp_field_name"]][:-4], '%Y/%m/%d %I:%M:%S %p',)
    survey.provided_availability = has_availability(survey)

    return survey


def read_survey(config: models.SurveyFieldMapping, data_file_path: str) -> list[models.SurveyRecord]:
    '''
    loads the data from the survey
    '''
    with open(data_file_path, 'r', encoding='utf-8-sig') as data_file:
        reader = csv.DictReader(data_file)
        surveys: list[models.SurveyRecord] = []
        for row in reader:
            survey = __parse_survey_record(config, row)

            skip_user = False
            for idx, existing_survey_record in enumerate(surveys):
                if existing_survey_record.student_id == survey.student_id:
                    if survey.submission_date > existing_survey_record.submission_date:
                        print(
                            f'found duplicate record for id: {existing_survey_record.student_id}. Using record with timestamp: {survey.submission_date}')
                        surveys[idx] = survey
                    else:
                        print(
                            f'skipped adding record with id: {existing_survey_record.student_id} and timestamp: {survey.submission_date}')
                    skip_user = True

            if not skip_user:
                surveys.append(survey)
    __preprocess_survey_data(surveys)

    return surveys


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
