#This demo takes a user input and handles it in the form of a rock paper scissor game
import random
move = input("Pick rock, paper, or scissors: ")
check = True;
user_move = ""
computer_move = ""

if (move == "rock" or move == "Rock"):
    print("You chose Rock.")
    user_move = "Rock"
elif(move == "paper" or move == "Paper"):
    print("You chose Paper.")
    user_move = "Paper"
elif(move == "scissors" or move == "Scissors"):
    print("You chose Scissors.")
    user_move = "Scissors"
else:
    print("Invalid move")
    check = False;
print()

if (check == True):
    computer_value = random.randint(1,3)
    if (computer_value == 1):
        computer_move = "Rock"
        print("Computer chose Rock.")
    elif (computer_value == 2):
        computer_move = "Paper"
        print("Computer chose Paper.")
    else:
        computer_move = "Scissors"
        print("Computer chose Scissors.")
    

    if (user_move == "Rock"):
        if(computer_move == "Rock"):
            print("It's a tie.")
        elif(computer_move == "Paper"):
            print("Player loses.")
        else:
            print("Player wins!!")
    elif(user_move == "Paper"):
        if(computer_move == "Rock"):
            print("Player wins!!")
        elif(computer_move == "Paper"):
            print("It's a tie.")
        else:
            print("Player loses.")
    else:
        if(computer_move == "Rock"):
            print("Player loses.")
        elif(computer_move == "Paper"):
            print("Player wins!!")
        else:
            print("It's a tie.")
else:
    print("Game can't run due to invalid user input.")