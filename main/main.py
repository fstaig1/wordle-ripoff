import random as r
from os import system


# function to let me easily clear the screen
def clear():
    system("cls")


# constants to store file locations
WORD_FILE = "main\\data\\sgb-words.txt"


# constants to store word list(ik they're technically not constants cos i instantly edit them but they never change after that)
WORD_LIST = []

# admin test vars
ENABLE_ADMIN_WORD = False
ADMIN_WORD = "WHEAT"


# generate word lists
with(open(WORD_FILE) as file):
    for line in file:
        WORD_LIST.append(line.split("\n")[0].split(" ")[0])


# pick word from answer list
def generateWord():
    return(WORD_LIST[r.randrange(0, len(WORD_LIST) - 1)])


# initialise game stuff idk yet
def initGame():
    global currentWord
    if not ENABLE_ADMIN_WORD:
        currentWord = generateWord()
        print("#############  CURRENT WORD - %s  ###############" % currentWord.upper())
    else:
        currentWord = ADMIN_WORD
        print("#############  ADMIN WORD - %s  ###############" % ADMIN_WORD.upper())


# user guessing
def guessWord():
    for guessNum in range(1, 7):

        valid = False

        while valid is False:
            print("\nGuess #%s." % guessNum)
            print("/ %s /" % generateWord())  # TODO remove

            guess = input("> ").lower()

            if guess in WORD_LIST:
                valid = True
            else:
                print("enter a valid 5 letter word")

        if guess == currentWord:
            winGame(guessNum=guessNum)
            break
        else:
            print(wordCheck(word=guess))


def wordCheck(word):  # TODO make this
    for i in word:
        print(i)
    return "TBD"


def winGame(guessNum):  # TODO make this
    print("You Win %s/6" % guessNum)


# main
def main():
    initGame()
    guessWord()


main()


input("\n\npause debugger :)")
