"""
Provides the ability to load data into the program including raw survey data and grouped data
"""

import csv

import datetime as dt
from typing import Union
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


def wildcard_availability(availability_fields: list) -> dict[str, list[str]]:
    '''
    constructs availability to match all of the time fields provided for any given day
    '''
    avail = {}
    for field in availability_fields:
        avail[field] = validate.WEEK_DAYS

    return avail


def has_availability(student: models.SurveyRecord) -> bool:
    '''
    checks if the student marked any days that they were available during the allotted time
    '''
    avail = 0
    for days in student.availability.values():
        avail += len(days)

    return avail > 0


def preprocess_survey_data(students: list[models.SurveyRecord], config: models.SurveyFieldMapping):
    '''
    performs some basic "preprocessing" of the survey data to ensure the grouping algorithm can function expected.
    This includes the following:
    - checking for students that didn't add availability and setting it to match any
    - checking for students that have availability that didn't match to anyone else's
    - checking for students that have preferred students that in turn disliked them (Not yet implemented)
    - checking for students that have preferred students that didn't match in their availability (Not yet implemented)
    '''
    for student in students:
        if not student.provided_availability:
            print(
                f"student '{student.student_id}' did not provide any availability")
            student.availability = wildcard_availability(
                config["availability_field_names"])
        if total_availability_matches(student, students) == 0:
            print(
                f"student '{student.student_id}' did not have matching availability with anyone else")
            student.has_matching_availability = False


def parse_survey_record(config: models.SurveyFieldMapping, row: dict) -> models.SurveyRecord:
    '''
    parses a survey record from a row in the dataset
    '''
    if not config.get('student_id_field_name') or len(row[config['student_id_field_name']]) == 0:
        raise AttributeError('student id not specified or is empty')

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
        avail_str = row[field].lower()
        survey.availability[field] = []
        if not avail_str == '':
            survey.availability[field] = avail_str.split(';')

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
    loads the data from the survey. 
    If there is a duplicate record, it will use the one with the submission date that is equal to or greater
    '''
    with open(data_file_path, 'r', encoding='utf-8-sig') as data_file:
        reader = csv.DictReader(data_file)
        surveys: list[models.SurveyRecord] = []
        for row in reader:
            survey = parse_survey_record(config, row)

            skip_user = False
            for idx, existing_survey_record in enumerate(surveys):
                if existing_survey_record.student_id == survey.student_id:
                    if survey.submission_date >= existing_survey_record.submission_date:
                        print(
                            f'found duplicate record for id: {existing_survey_record.student_id}. Using record with timestamp: {survey.submission_date}')
                        surveys[idx] = survey
                    else:
                        print(
                            f'skipped adding record with id: {existing_survey_record.student_id} and timestamp: {survey.submission_date}')
                    skip_user = True

            if not skip_user:
                surveys.append(survey)
    preprocess_survey_data(surveys, config)

    return surveys


def read_groups(group_file: str, survey_data: list[models.SurveyRecord]) -> list[models.GroupRecord]:
    '''
    Reads in grouping data into a list of GroupRecord objects
    '''
    groups: dict[str, models.GroupRecord] = {}
    is_header: bool = False
    with open(group_file, 'r', encoding='utf-8-sig') as data_file:
        reader = csv.DictReader(data_file)

        for row in reader:

            if is_header:
                is_header = False
                continue

            group_id = row["group id"]

            if not group_id in groups:
                groups[group_id] = models.GroupRecord(group_id, [])

            user = __get_user_by_id(row["student id"], survey_data)

            if not user is None:
                groups[group_id].members.append(user)

    return list(groups.values())

def __get_user_by_id(student_id: str, survey_data: list[models.SurveyRecord]) -> Union[models.SurveyRecord, None]:
    '''
    Gets a SurveyRecord based on the student id
    '''

    for user in survey_data:
        if user.student_id == student_id:
            return user

    return None

def add_missing_students(survey: list[models.SurveyRecord], roster: list[str], avail_field: list[str]) -> list[models.SurveyRecord]:
    '''
    This method involves reading the survey data and adding any missing students from the student list
    to the survey data. This will be based on student id.
    '''
    new_survey_data = survey
    survey_students = list(map(lambda x: x.student_id, survey))

    #At this point, the survey_student list should have every student name from the survey data.
    #Next, we will check if all the students have answered the survey.

    missing_students = []
    for student in roster:
        if survey_students.count(student) == 0:
            missing_students.append(student)

    #At this point, all missing students should be in the missing students list.
    for asurite in missing_students:
        record = models.SurveyRecord (
            student_id=asurite,
        )
        #This code will use the function that adds availiability to all time slots.
        record.availability = wildcard_availability(avail_field)
        record.provided_survey_data = False
        record.provided_availability = False
        record.has_matching_availability = False
        new_survey_data.append(record)

    return new_survey_data

def read_roster(filename: str) -> list[str]:
    '''
    This method reads the roster file and returns the full roster of students
    '''
    roster = []

    with open(filename, 'r', encoding='utf-8-sig') as data_file:
        reader = csv.reader(data_file)
        next(reader)
        for row in reader:
            roster.append(row[0])
    
    return roster
