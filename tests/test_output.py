'''
Output tests
'''
import csv
import os
from app import output

def test_output_to_csv():
    '''
    Test the output WriteSurveyData
    '''
    filepath = 'tests/testout.csv'
    headers = ['hi', 'my', 'name', 'is', 'zach' ]
    body = [['a', 'b', 'c', 'd', 'e'], ['a', 'b', 'c', 'd', 'e'],
            ['a', 'b', 'c', 'd', 'e']]

    writer = output.WriteSurveyData()
    writer.output_to_csv(headers, body, filepath)

    with open(filepath, 'r',  encoding="UTF-8") as file:
        reader = csv.reader(file)
        assert next(reader) == headers

    os.stat(filepath)
    os.remove(filepath)
    