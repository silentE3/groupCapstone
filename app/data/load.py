""" SurveyDataReader will read in the survey data from the dataset CSV file and parse it based on the
grouping config. The first line of the dataset data is assumed to be header data.
    GroupingDataReader will read in the grouping data from a CSV file and parse it.
The first line of the dataset data is assumed to be header data."""

import csv
from app import models


class SurveyDataReader():
    '''
    provides a reader for parsing the raw data from surveys
    '''

    def __init__(self, configuration: models.SurveyFieldMapping) -> None:
        self.config = configuration

    def load(self, data_file_path: str) -> list[models.SurveyRecord]:
        '''
        loads the data from the survey
        '''
        with open(data_file_path, 'r', encoding='utf-8-sig') as data_file:
            reader = csv.DictReader(data_file)
            surveys: list[models.SurveyRecord] = []
            for row in reader:
                preferred_students: list[str] = []
                disliked_students: list[str] = []
                for field in self.config['preferred_students_field_names']:
                    if row[field] != "":
                        preferred_students.append(row[field])

                for field in self.config['disliked_students_field_names']:
                    if row[field] != "":
                        disliked_students.append(row[field])

                availability: dict[str, list[str]] = {}
                for field in self.config['availability_field_names']:
                    availability[field] = row[field].split(';')

                timezone = ''
                if self.config.get('timezone_field_name') and row[self.config['timezone_field_name']] != '':
                    timezone = row[self.config['timezone_field_name']]

                survey = models.SurveyRecord(
                    row[self.config['student_id_field_name']],
                    timezone,
                    preferred_students,
                    disliked_students,
                    availability
                )

                surveys.append(survey)

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
