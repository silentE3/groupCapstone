# For the purpose of this demo, the following will be known (assumed) about the CSV text:
# 	- The first line will contain a brief description (header) of the elements (comma-separated)
# 		that are provided for/by each student.
# 	- Each subsequent line will define the values of the elements for a single student
# 	- Each comma separated value is enclosed in quotes

# Additionally, reading of an input text file is covered via a separate demo. Therefore,
# the CSV text will be hard-coded as follows:
csv_text = '''"Timestamp","Username","Please select your ASURITE ID","Please enter your Github username (NOT your email address)","Email address","In what time zone do you live or will you be during the session? Please use UTC so we can match it easier.","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [0:00 AM - 3:00 AM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 AM - 6:00 AM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 AM - 9:00 AM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 AM - 12:00 PM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [12:00 PM - 3:00 PM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [3:00 PM - 6:00 PM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [6:00 PM - 9:00 PM]","Please choose times that are good for your team to meet. Times are in the Phoenix, AZ time zone! [9:00 PM - 12:00 PM]","How well would you say you know GitHub? (1 not at all, 5 worked with it a lot - know how to merge, resolve conflicts, etc.) You are not expected to know GitHub well yet, so please be honest. It will not be used for grading what you put here but I want to try to have one student knowing GitHub in each team to make things easier.","Do you know Scrum already? (1 just heard about it, 5 know it well (process, roles). You are not expected to know Scrum yet, so please be honest. It will not be used for grading what you put here. ","Preferred team member 1","Preferred team member 2","Preferred team member 3","Preferred team member 4","Preferred team member 5","Non-preferred student 1","Non-preferred student 2","Non-preferred student 3"
"2022/10/17 6:31:58 PM EST","alphaone1@asu.edu","alphaone1","alphaOne_1","alphaone1@gmail.com","UTC +1","Sunday","Monday","","","","","","","5","2","betatwo2 - Beta Two","","","","","gammathree3 - Gamma Three","",""
"2022/10/17 6:33:27 PM EST","betatwo2@asu.edu","betatwo2","betatwo_2","betatwo2@gmail.com","UTC +2","","","","","Tuesday","Wednesday","","","4","3","gammathree3 - Gamma Three","","","","","alphaone1 - Alpha One","",""
"2022/10/17 6:34:15 PM EST","gammathree3@asu.edu","gammathree3","gammathree_3","gammathree3@gmail.com","UTC +3","","","","","","","Thursday","Friday","3","4","alphaone1 - Alpha One","","","","","betatwo2 - Beta Two","",""'''

# The CSV text will be processed/stored as follows:
#	The description/header for each element will be stored in a list.
#	A student object will be created for each student (non-first line) in the
#		file, which simply contains a list of the values for that student.
#	The student objects will be stored in a 'students' list.

#####
# Define the Student class
class Student:
	def __init__(self):
		self.values = []; # List to store the student's values

#####
# Create the headers list
headers = [];

#####
# Create the students list
students = []

#####
# Split the stored string by line breaks (to have a separate string for each line)
lines_list = csv_text.split("\n")

#####
# Parse the strings in the lines list

for idx,line in enumerate(lines_list):
	# Split the line's comma separated values into individual values (stored in a list)
	separatedVals = line.split('","') # "," rather than just , to ignore commas within the values
	
	#remove residual quotation mark from start and end elements
	if len(separatedVals) > 0:

		separatedVals[0] = separatedVals[0].replace('"','')
		separatedVals[-1] = separatedVals[-1].replace('"','')

	if (idx == 0): #first line -- headers
		for value in separatedVals:
			headers.append(value)
	else:
		student = Student() #create the student object

		#store the student's values
		for value in separatedVals:
			student.values.append(value) 
		
		students.append(student) # add the student to the students list

# In this demo, we'll print the results to show it's working

#####
# Print the headers, one on each line
print("***** HEADERS *****")
for header in headers:
	print(header)
print("\n")

#####
# Print the values for each Student
for idx,student in enumerate(students):
	print("***** Student " + str(idx + 1) + " *****")
	for value in student.values:
		print(value)
	print("\n")
