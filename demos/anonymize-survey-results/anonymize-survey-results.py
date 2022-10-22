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

#Get and parse program args
argCnt = len(sys.argv)
if argCnt < 2:
	print("USAGE: python anonymize-survey-results.py <RawResults>.csv")
	quit()

filename = os.path.basename(sys.argv[1])

raw_results = []
with open(filename, newline='') as input_file:
	reader = csv.reader(input_file)
	raw_results = list(reader)

# asurite data dictionary key:value = original:new/fake
asuriteDict = {}

for index,line in enumerate(raw_results):
	if index == 0 or len(line) < 24: #headers or non-conforming data
		continue

	# Generate fake new asurite for the student
	newAsurite = "asurite" + str(index)
	
	if line[2] != "": #asurite
		asuriteDict[line[2]] = newAsurite

studentCount = len(raw_results) - 1
for index,line in enumerate(raw_results):
	if len(line) < 24:
		print("WARNING: Non-conforming data (less than 24 comma-separated elements) found on line " + str(index + 1) + ". Line skipped.")
		continue
	if index == 0: #headers
		continue

	# Generate fake new identifiers for the student
	newName = "A" + str(index)
	newAsurite = "asurite" + str(index)
	newGithub = "A_" + str(index)

	# index 0: timestamp -- do nothing
	
	# index 1: username
	if line[1] != "":
		line[1] = newAsurite + "@asu.edu"
	
	# index 2:
	#asurite ID
	if line[2] != "":
		line[2] = newAsurite
	
	# index 3:
	#Github username
	if line[3] != "":
		line[3] = newGithub
	
	# index 4:
	#email address
	if line[4] != "":
		line[4] = newName + "@gmail.com"
	
	# index 5: time zone -- do nothing
	# index 6 - 13: Availability slots -- do nothing
	# index 14 & 15: Skills rating -- do nothing

	# 16 - 23: preferred and non-preferred students	
	for num in range(16,24):
		element = line[num]
		if element != "" and not(element in asuriteDict):
			elementParts = line[num].split(' ')
			# first element of parts is asurite
			if elementParts[0] in asuriteDict:
				line[num] = asuriteDict[elementParts[0]]
			else:
				# add to asurite dictionary
				studentCount += 1
				asuriteDict[elementParts[0]] = "asurite" + str(studentCount)
				#replace this instance
				line[num] = asuriteDict[elementParts[0]]
	
	# replace the original data with the anonymized data					
	raw_results[index] = line

# write the anonymized data out to <origFilename>_Anon.csv
filename_parts = filename.split('.')
with open(filename_parts[0] + "_Anon.csv", 'w', newline='') as output_file:
	writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
	for row in raw_results:
		writer.writerow(row)