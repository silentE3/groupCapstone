file1 = open("readTest.txt", "r");

#This part will consist of expressions that get the number of lines in the text file.
count = len(file1.readlines())
print("Number of lines: " + str(count))

#This part consists of getting every line in the text file one by one using a for loop.
for line in file1:
        n_line = line.strip();
        print(n_line);
file1.close();

file2 = open("readTest.txt", "r");

#This part consists of printing out every single line at once as an array.
print(file2.readlines())


