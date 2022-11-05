"""
manages outputs for the program
"""

import csv

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
