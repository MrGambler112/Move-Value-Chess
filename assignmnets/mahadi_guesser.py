#Name: The Auto Guesser
#Programmer: Syed (Mahadi) Masuduzzaman
#Date: March 25, 2026
#Description: Guessing Game where user guesses the correct car company

import random

print ("The Auto Guesser\n")
print ("Welcome to The Auto Guesser where you must guess the correct companies"
         " according to their countries of origin\n")

print ("\\ *** \\    -----                 /\\     |      |    ---------   /      \\ \n")
print (" \\ *** \\     /|_||_|\\__         /  \\    |      |        |      |        |\n")
print ("  \\ *** \\  (  > | >|  \\)       /____\\   |      |        |      |        |\n")
print ("   \\  *   ==-(_)---(_) _\\)     /      \\   \\____/         |      \\___ ___/ \n")


player_name = input("Before we begin, what is your name?: ")

choice = random.randrange(10)

if choice == 0:
    answer = "toyota"
    hint = "Japan"

elif choice == 1:
    answer = "maserati"
    hint = "Italy"

elif choice == 2:
    answer = "ford"
    hint = "United States"

elif choice == 3:
    answer = "kia"
    hint = "South Korea"

elif choice == 4:
    answer = "mercedes"
    hint = "Germany"

elif choice == 5:
    answer = "land rover"
    hint = "United Kingdom"

elif choice == 6:
    answer = "byd"
    hint = "China"

elif choice == 7:
    answer = "volvo"
    hint = "Sweden"

elif choice == 8:
    answer = "bugatti"
    hint = "France"

else:
    answer = "lexus"
    hint = "Japan"

print ("\nHint: The car company is from the country: ", hint, "\n")

max_guesses = int(input(player_name + ", how many guesses would you like to have?: "))

i = 0
correct = True

while correct:  
        user_answer = input("Guess the car company from " + hint + 
            " (lowercase answer please):")
        i = i + 1
        if user_answer == answer:
            correct = False
            print (player_name, "guessed correctly, you win!")
        if i == max_guesses:
            correct = False
            print ("\n", player_name, "fails to guess the car company in" 
                " the allotted number of guesses")
        if i != max_guesses:
            if user_answer != answer:
                print ("Wrong guess", player_name, "! try again.")

input ()