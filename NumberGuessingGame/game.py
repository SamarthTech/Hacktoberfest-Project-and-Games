from random import randint

answer = randint(1, 9)

user_input = int(input("Guess any number between 0 and 10\n"))

numberOfGuesses = 2

while numberOfGuesses > 0:
    if user_input == answer:
        print("CORRECT")
        user_input = int(input(""))

    elif user_input > answer:
        print("The number is smaller, Guess Again")
        user_input = int(input(""))
        numberOfGuesses -= 1

    elif user_input < answer:
        print("The number is bigger, Guess Again")
        user_input = int(input("")) 
        numberOfGuesses -= 1