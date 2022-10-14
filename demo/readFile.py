file1 = open("readTest.txt", "r");

#This part consists of getting every line in the text file one by one using a for loop.
for line in file1:
        n_line = line.strip();
        print(n_line);


#This part will consist of expressions that get the number of lines in the text file.