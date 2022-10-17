#Python tutorial link: https://www.youtube.com/watch?v=kqtD5dpn9C8

#Part 1: Hello World
print("Hello World")

#Part 2: Variable types
age = 20
price = 19.95
first_name = "Mark"
is_online = False
print(age)

#Part 3: Input
#response = input("What is your name? ")
#print("Hello " + response)

#Part 4: Type conversion
birth_year = input("Enter your birth year: ")
#age2 = 2020 - birth_year Causes an error due to type difference.
age2 = 2022 - int(birth_year)
print(age2)

#time1 = input("First trial: ")
#time2 = input("Second trail: ")
#difference_time = int(time2) - int(time1)
#print(str(difference_time))

#Part 5: Strings
test = "Make sure to focus on your homework on SER 401"
print(test.find("focus")) #Gets the index of the word focus.
print("401" in test) #Checks if a word is in a string.

#Part 6: Arithmetric Operators
print(10 % 3)
print(10 ** 3) #exponent: in this case 10 to the power of three.

x = 5
x += 3
print(x) #Result should be 8

#Part 7: Operation Precedence
#Same as math. PEMDAS

#Part 8: Comparison Operators
#Same as the ones in Java.

#Part 9: Logical Operators
# and statement: and
# not statement: not
# or statement: or

#Part 10: If statements
temperature = 68

if temperature > 85:
    print("Man, it's hot out here.")
elif temperature < 85 and temperature > 69:
    print("This is normal.")
else:
    print("Man, it's cold out here.")

#Part 11: Exercise
weight = input("Weight: ")
units = input("(K)g or (L)bs? ")

if units.upper() == "K" or units.lower() == "k":
    result = int(weight) / 0.45
    print(result)
elif units.upper() == "L" or units.lower() == "l":
    result = int(weight) * 0.45
    print(result)

#Part 12: While Loops
i = 1
while i <= 5:
    print(i)
    i = i + 1

j = 1
while j <= 10:
    print(j * "*")
    j = j + 1

#Normally, we don't combine strings and ints, but the second while loop is multiplying the number of the string by j.

#Part 13 and 14: Lists and List methods
names = ["Mark", "John", "Eliza", "Falco"]
print(names[2])
print(names[-1]) #A negative number index starts at the end of the list. In this case, index of 3 would be -1 as well.
print(names[0:2]) #Gets all the elements in the list from index 0 to 2.

names.append("Edward") #Adds a new element to the list.
print(names)
names.insert(0, "Maria") #Adds a new element at a given index
print(names)
names.remove("John") #Removes an element in the list
print(names)
names.clear() #Clears the whole list
print(names)

#Part 15: For loop
numbers = [1, 2, 3, 4, 5, 6, 7]
#This for loop prints out methods
for item in numbers:
    print(item)

#Part 16: Range function
#The range function creates a range object from a start and end value.
#We can use a for loop to go through all of the values in the range object.
#This method also has a step parameter that gets values from the range object while jumping by a given number.
#In the tutorial, the step parameter made the range method get 5, 7, and 9 from the range object range(5,10).

#Part 17: Tuples
#Defined by surrounding the values with ().
#Tuples are unchangeable!!!
#You can get the number of a given value and the elements in a tuple at a given index, but that's it.