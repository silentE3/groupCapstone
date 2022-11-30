"""
manages outputs for the program
"""

import csv
from app import models


class WriteSurveyData:
    '''
    This class outputs generated test survey data to a csv
    '''

    def output_to_csv(self, headers: list[str], body, filename: str):
        """
        saves data to a csv file given the headers, body rows, and filename to save to.
        """

        with open(filename, 'w', newline='\n', encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(body)


class GroupingDataWriter:
    '''
    This class outputs a list of group data to a csv
    '''

    def __init__(self, configuration: models.Configuration) -> None:
        self.config = configuration

    def write_csv(self, groups: list[models.GroupRecord], filename: str):
        '''
        Outputs group data, from a list to a csv using the config file for fields
        '''

        header = self.__create_header()
        body = self.__create_body(groups)

        with open(filename, 'w', newline='\n', encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(body)

    def __create_body(self, groups: list[models.GroupRecord]) -> list[list[str]]:
        '''
        Create a body from the config data
        '''
        group_id = 0
        body = []
        for group in groups:
            group_id += 1

            for member in group.members:
                entry = []
                # group
                entry.append(f"group_{group_id}")
                # id
                entry.append(member.student_id)
                # name
                if self.config.get("output_student_name"):
                    entry.append(member.student_name)
                # email
                if self.config.get("output_student_email"):
                    entry.append(member.student_email)
                # login
                if self.config.get("output_student_login"):
                    entry.append(member.student_login)
                body.append(entry)
        return body

    def __create_header(self) -> list[str]:
        '''
        Create a header from the config
        '''
        header = []

        header.append("group id")
        header.append("student id")
        # name
        if self.config.get("output_student_name"):
            header.append("student name")
        # email
        if self.config.get("output_student_email"):
            header.append("student email")
        # login
        if self.config.get("output_student_login"):
            header.append("student login")

        return header
