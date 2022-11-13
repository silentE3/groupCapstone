# ********************************************
# This program is used to anonymize raw .csv survey results that have
# the following format:
#
# First line: Timestamp,Username,Please select your ASURITE ID,Please enter your Github username (NOT your email address),Email address,In what time zone do you live or will you be during the session? Please use UTC so we can match it easier.,"Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]","How well would you say you know GitHub? (1 not at all, 5 worked with it a lot - know how to merge, resolve conflicts, etc.) You are not expected to know GitHub well yet, so please be honest. It will not be used for grading what you put here but I want to try to have one student knowing GitHub in each team to make things easier.","Do you know Scrum already? (1 just heard about it, 5 know it well (process, roles). You are not expected to know Scrum yet, so please be honest. It will not be used for grading what you put here. ",Preferred team member 1,Preferred team member 2,Preferred team member 3,Preferred team member 4,Preferred team member 5,Non-preferred student 1,Non-preferred student 2,Non-preferred student 3
#
# Subsequent lines: define results for a single student per line
#
# Preferred and non-preferred student entries have the format:
# "<asurite> - <First Name> <Last Name>"
#
# *********************************************
# Program Usage:
# python anonymize-survey-results.py <RawResults>.csv
#
# Output is: Anonymized results as <RawResults>_Anon.csv

import csv
import os
import sys

# Get and parse program args
argCnt = len(sys.argv)
if argCnt < 2:
    print("USAGE: python anonymize-survey-results.py <RawResults>.csv")
    quit()

filename = os.path.basename(sys.argv[1])

raw_results = []
with open(filename, 'r', newline='', encoding='utf-8-sig') as input_file:
    reader = csv.reader(input_file)
    raw_results = list(reader)

# analyze the headers for certain expected columns
headers: list[str] = raw_results[0]

username_col: int
try:
    username_col = next(idx for idx, element in enumerate(
        headers) if element.lower() == 'username')
except StopIteration:
    username_col = -1

asurite_col: int
try:
    asurite_col = next(idx for idx, element in enumerate(
        headers) if "asurite" in element.lower())
except StopIteration:
    print("Error!! No column containing 'asurite' found. Program terminated.")
    quit()

github_username_col: int
try:
    github_username_col = next(idx for idx, element in enumerate(
        headers) if "github username" in element.lower())
except StopIteration:
    github_username_col = -1

email_col: int
try:
    email_col = next(idx for idx, element in enumerate(
        headers) if element.lower().startswith("email address"))
except StopIteration:
    email_col = -1

preferences_cols: list[int] = [idx for idx, element in enumerate(
    headers) if "preferred" in element.lower()]

# Some datasets appeared to contain extraneous data in unlabeled columns. Flag
#	this data to be skipped when writing the anonymized output.
unidentified_cols: list[int] = [idx for idx, element in enumerate(
    headers) if element == ""]
unidentified_cols.sort(reverse=True)  # sort in descending order

# Build asurite data dictionary key:value = original:new/fake
asurite_dict = {}
for index, line in enumerate(raw_results):
    if index == 0:  # skip headers row
        continue

    # Generate fake new asurite for the student
    NEW_ASURITE: str = "asurite" + str(index)

    if line[asurite_col] != "":
        asurite_dict[line[asurite_col]] = NEW_ASURITE

# Anonymize the necessary columns
studentCount = len(raw_results) - 1
for index, line in enumerate(raw_results):
    if index != 0:  # skip headers row

        # Generate fake new identifiers for the student
        NEW_NAME: str = "A" + str(index)
        NEW_ASURITE: str = "asurite" + str(index)
        NEW_GITHUB = "A_" + str(index)

        # username
        if username_col != -1 and line[username_col] != "":
            line[username_col] = NEW_ASURITE + "@asu.edu"

        # asurite ID
        if line[asurite_col] != "":
            line[asurite_col] = NEW_ASURITE

        # Github username
        if github_username_col != -1 and line[github_username_col] != "":
            line[github_username_col] = NEW_GITHUB

        # email address
        if email_col != -1 and line[email_col] != "":
            line[email_col] = NEW_NAME + "@gmail.com"

        # preferred and non-preferred students
        for num in preferences_cols:
            element = line[num]
            if element != "" and not element in asurite_dict:
                elementParts = line[num].split(' ')
                # first element of parts is asurite
                if elementParts[0] in asurite_dict:
                    line[num] = asurite_dict[elementParts[0]]
                else:
                    # add to asurite dictionary
                    studentCount += 1
                    asurite_dict[elementParts[0]] = "asurite" + \
                        str(studentCount)
                    # replace this instance
                    line[num] = asurite_dict[elementParts[0]]

    # Delete unidentified data (columns)
    for num in unidentified_cols:
        del line[num]

    # replace the original data with the anonymized data
    raw_results[index] = line

# write the anonymized data out to <origFilename>_Anon.csv
filename_parts = filename.split('.')
with open(filename_parts[0] + "_Anon.csv", 'w', newline='', encoding='utf-8-sig') as output_file:
    writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
    for row in raw_results:
        writer.writerow(row)
