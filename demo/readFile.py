file1 = open("readTest.txt", "r");

#You can't have any other readlines() unless you close the file first
content = file1.readlines()

#This part will consist of expressions that get the number of lines in the text file.
count = len(content)
print("Number of lines: " + str(count))

file1.close();

#This part consists of printing out every single line at once.
print(content)

#This part consists of printing out every single line in the content(list) by index
print(content[0])
print(content[1])
print(content[2])


