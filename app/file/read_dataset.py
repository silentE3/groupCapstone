"""This will read in the survey data from the dataset CSV file and parse it based on the 
grouping config. The first line of the dataset data is assumed to be header data."""

import csv
from app.data_classes import config, survey_data


class SurveyDataReader():
    '''
    provides a reader for parsing the raw data from surveys
    '''

    def __init__(self, configuration: config.GroupingConfig) -> None:
        self.config = configuration

    def load(self, data_file_path: str) -> list[survey_data.SurveyData]:
        '''
        loads the data from the survey
        '''
        with open(data_file_path, 'r', encoding='utf-8') as data_file:
            reader = csv.DictReader(data_file)
            surveys: list[survey_data.SurveyData] = []
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

                survey = survey_data.SurveyData(
                    row[self.config['student_id_field_name']],
                    row[self.config['timezone_field_name']],
                    preferred_students,
                    disliked_students,
                    availability
                )

                surveys.append(survey)

        return surveys
