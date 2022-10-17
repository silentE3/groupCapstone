"""
manages outputs for the program
"""

import csv
from typing import List


def output_to_csv(headers: List[str], body: List[List[str]], filename: str):
    """
    saves data to a csv file given the headers, body rows, and filename to save to.
    """

    with open(filename, 'w', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(body)
