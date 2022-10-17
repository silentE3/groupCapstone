#This part is used to print out "Hello World"
print("Hello World")

#This part consists of creating a basic class that contains a number, string, and boolean
class test:
    x = 3
    ex = "Example"
    check = True #Boolean values must be uppercased

pt = test();
print("This is " + pt.ex + " " + str(pt.x)) #If you want to print out a sentence/string with a number, you must do str(number)
print(pt.check)

#This part consists of creating a basic class that requires 2 int parameters
class test2():
    num1 = 0
    num2 = 0

    def __init__(self, testNum1, testNum2):
        self.num1 = int(testNum1)
        self.num2 = int(testNum2)

#This should run correctly.    
#group1 = test2(3, 2)
#print("Test2 construction 1")
#print(group1.num1)
#print(group1.num2)

#This should throw an error since one of the parameters is a string.
#group2 = test2("test", 2)
#print("Test2 construction 2")
#print(group2.num1)
#print(group2.num2)

#This should throw an error since it has no parameters at all due to no default constructor.
#group3 = test2()
#print("Test2 construction 3")
#print(group3.num1)
#print(group3.num2)

class calculator():
    cnum1 = 0
    cnum2 = 0
    operator = ""
    result = 0

#Learned that you can only have 1 constructor in Python.
    def __init__(self, num1, num2, operand):
        self.cnum1 = num1;
        self.cnum2 = num2;
        self.operator = operand;

    classmethod
    def calculate(cls, num1, num2, operand):
        if(operand == "add"):
            cls.result = num1 + num2;
        elif(operand == "subtract"):
            cls.result = num1 - num2;
        elif(operand == "multiply"):
            cls.result = num1 * num2;
        elif(operand == "divide"):
            cls.result = num1 / num2;

set = calculator(0, 0, "");
set.calculate(2, 3, "add");
print(set.result); #The result should be 5.

set.calculate(7, 4, "subtract");
print(set.result) #The result should be 3.

set.calculate(8, 5, "multiply");
print(set.result) #The result should be 40.

set.calculate(16, 4, "divide");
print(set.result) #The result should be 4.

set.calculate(1, 2, "divide");
print(set.result) #The result should be 0.5.