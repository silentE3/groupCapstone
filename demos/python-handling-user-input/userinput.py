#This demo is in the form of a grading program that given a grade based on the value given.
grade_percent = input("Enter in your grade percent: ")

try:
    if (int(grade_percent) >= 90):
        print("You got an A!!")
    elif(int(grade_percent) < 90 and int(grade_percent) >= 80):
        print("You got a B!")
    elif(int(grade_percent) < 80 and int(grade_percent) >= 70):
        print("You got a C.")
    elif(int(grade_percent) < 70 and int(grade_percent) >= 60):
        print("You got a D.")
    else:
        print("You got an E")
except:
    print("Invalid input")
