# In The Name Of God
# Studernt Name: Rasoul Soltanzadeh
# Student ID: 40413160281816
# Teacher Name: Dr. Afrabandpay
# University: University Of Mazandaran 
# Field Of Study: Computer Engineerung 
# Term: 2
# Course: Advanced Programing
# Modify Date: 1405/1/31/4:45 - 2026/4/20/4:45
# Language Version: Python 3.11 (64-bit) 
# Subject: word_game application
from string import *
from helper import *


## Constants ##

MAX_MISTAKES = 6

## State variables ##

secret_word = random_secret_word()    # from word guess_lib
letters_guessed = []    # empty list -- no letters guessed initially
mistakes_made = 0
dashed_word = secret_word.__len__() * '-'
last_letter = ''
turns = 0

## Helper functions ##

def word_guessed():
    """ Returns True if the player has successfully guessed the word otherwise False. """
    return dashed_word.count('-') == 0

def guessed_so_far():
    """ Returns a string of the word with not-guessed letters as dashes. """
    result = ""
    for i in range(secret_word.__len__()):  result += secret_word[i] if last_letter == secret_word[i] else dashed_word[i] 
    return result
        

## Main game code ##

# Some intro stuff...

print("Welcome to word guess!")
print()

first_time = input("Is this your first time playing word guess? (y/n) ")

print()

if first_time == "y":
    # it's their first time -- let's give them instructions.
    print("The objective of word guess is to guess a secret word letter by letter.")
    print("If you guess a letter in the word, we'll show you that letter.")
    print("But if you guess wrong, we'll the number remaining wrong guesses you have.")
    print("You should guess the word before remaining wrong guesses reaches 0, or else you lose!")
    print()

print("Great, so you're ready to play. Just two things that might help:")
print("1) The secret word has", len(secret_word), "letters.")
print("2) It takes", MAX_MISTAKES, "wrong guesses to lose.")
print()
print("Good luck!")
print()
print("[Press enter when ready to play.]")
input()     # this just waits for them to press enter... they can type
            # other stuff but it doesn't affect anything.


''' On to our game ... Here you need to write the body of your code.
The game terminates either by losing (hitting MAX_MISTAKES), or by
winning (guessing the correct word before reaching the MAX_MISTAKES).
So, you need to continue the word guessing process until one of the
above condition met.'''

### To Do ###
### Write your code here ###

print()
print("The word so far: _ _ _ _ _ _ _ ")
print("Letters guessed so far:")
print(f"Wrong guesses remaining: {MAX_MISTAKES}")
print()

while ((MAX_MISTAKES > 0) and (not word_guessed())):
    turns += 1
    print("What letter do you guess?")
    last_letter = input()
    letters_guessed.append(last_letter)
    dashed_word_backup = dashed_word
    dashed_word = guessed_so_far()
    b = (dashed_word_backup == dashed_word)
    MAX_MISTAKES -= b
    mistakes_made += b
    print(f"Good guess! {last_letter} is in the word." if(not b) else f"Wrong! {last_letter} is not in the word.")
    print(f"The word so far: {' '.join(dashed_word)}")
    print(f"Letters guessed so far: {last_letter}")
    print(f"Wrong guesses remaining: {MAX_MISTAKES}")
    print()

'''Now we're out of the body of the game. As we said above, this means either we
guessed wrong too many times, or we won. Check and inform the user. '''

### To Do ###
### Write your code here ###

print("Very good. You won." if word_guessed() else "Oh, you faild")
print(f"Your had {mistakes_made} mistakes. And {turns - mistakes_made} true-guesses. In {turns} turns.\n And the word was {secret_word}. And you guessed in as far as {dashed_word}.")