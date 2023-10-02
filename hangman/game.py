import random

# List of words to choose from
word_list = ["apple", "banana", "cherry", "orange", "grape", "strawberry", "blueberry"]

# Select a random word from the list
chosen_word = random.choice(word_list)

# Convert the chosen word to a list of characters
word_letters = list(chosen_word)

# Initialize the display word with underscores
display_word = ["_"] * len(chosen_word)

# List to keep track of guessed letters
guessed_letters = []

# Number of chances the player has
lives = 6

while True:
    # Print current state of the game
    print(" ".join(display_word))
    print(f"Guessed letters: {' '.join(guessed_letters)}")
    
    # Ask the player to guess a letter
    guess = input("Guess a letter: ").lower()

    if guess in guessed_letters:
        print("You've already guessed that letter.")
        continue
    
    if guess in word_letters:
        # Update display_word with correctly guessed letters
        for i in range(len(chosen_word)):
            if word_letters[i] == guess:
                display_word[i] = guess
    else:
        # Reduce a life for incorrect guesses
        lives -= 1
        print(f"Wrong guess! You have {lives} lives left.")
    
    guessed_letters.append(guess)

    # Check if the player has won or lost
    if "_" not in display_word:
        print("Congratulations! You've won!")
        break
    elif lives == 0:
        print(f"Sorry, you've run out of lives. The word was '{chosen_word}'.")
        break
