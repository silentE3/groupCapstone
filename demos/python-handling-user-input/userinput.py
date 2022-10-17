#This demo is in the form of a grading program that given a grade based on the value given.
grade_percent = input("Enter in your grade percent: ")

if (grade_percent >= 90):
    print("You got an A!!")
elif(grade_percent < 90 and grade_percent >= 80):
    print("You got a B!")
elif(grade_percent < 80 and grade_percent >= 70):
    print("You got a C.")
elif(grade_percent < 70 and grade_percent >= 60):
    print("You got a D.")
else:
    print("You got an E")