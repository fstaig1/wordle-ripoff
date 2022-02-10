import random as r
from os import system
import re
from models import Letter


# function to let me easily clear the screen
def clear():
    system("cls")


# constants to store file locations
WORD_FILE = "data\\sgb-words.txt"


# constant to store list of words
WORD_LIST = []
with(open(WORD_FILE, "r") as file):
    for line in file:
        WORD_LIST.append(line.split("\n")[0].split(" ")[0])


# constant for alphabet + generating letters dict
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
global letters
letters = {}
for i in ALPHABET:
    letters.update({i: -1})
print(letters)


# admin test vars
ENABLE_ADMIN_WORD = False
ADMIN_WORD = "skill"
ENABLE_ADMIN_PRINTS = False
ENABLE_EMOJI_PRINTS = True


# function to print if admin prints are enabled
def adminPrint(string):
    if ENABLE_ADMIN_PRINTS:
        print(string)


def emojiPrint(list):
    """function to return scores as emojis

    Args:
        list list[int]: list of integers equal to either 0, 1 or 2
    """
    if ENABLE_EMOJI_PRINTS and not ENABLE_ADMIN_PRINTS:

        emojis = ["⬛", "🟨", "🟩"]
        string = ""
        for i in list:
            string += emojis[i]
        return(string)
    else:
        return(list)


# pick word from answer list
def generateWord():
    return(WORD_LIST[r.randrange(0, len(WORD_LIST) - 1)])


# initialise game stuff idk yet
def initGame():
    global currentWord
    if not ENABLE_ADMIN_WORD:
        currentWord = generateWord()
        adminPrint("#############  CURRENT WORD - %s  #############" % currentWord.upper())
    else:
        currentWord = ADMIN_WORD
        adminPrint("#############  ADMIN WORD - %s  #############" % ADMIN_WORD.upper())


# user guessing
def guessWord():
    scores = []
    for guessNum in range(1, 7):
        valid = False

        while not valid:
            print("\nGuess #%s." % guessNum)
            adminPrint("/ %s /" % generateWord())
            if guessNum > 1:
                for i in scores:
                    print("%s %s" % (emojiPrint(i[0]), i[1].upper()))

            guess = input("> ").lower()

            if guess in WORD_LIST:
                valid = True
            else:
                print("enter a valid 5 letter word")
        score = wordCheck(word=guess)

        scores.append(score)
        if score[0] == [2, 2, 2, 2, 2]:
            winGame(scores)
            break
    loseGame(scores)


def wordCheck(word):
    """Function to check letter pos in word in reference to currentWord.

    Args:
        word (str): 5 letter string

    Returns:
        list[int]: 5 ints which refer to each letters score -
                        2 = green, 1 = yellow, 0 = grey
    """
    list = []

    for num in range(0, len(word)):
        adminPrint("\n num %s" % num)
        letter = word[num]
        score = 0
        # check if letter in word
        if letter in currentWord:
            adminPrint("%s in %s" % (letter, currentWord))
            winPos = [char.start() for char in re.finditer(letter, currentWord)]
            guessPos = [char.start() for char in re.finditer(letter, word)]
            adminPrint("pos %s" % (winPos))
            for i in winPos:
                adminPrint("word[i] %s currentWord[num] %s" % (word[i], currentWord[num]))
                # check if letter in exact pos
                if word[i] == currentWord[num]:
                    adminPrint("%s in %s at pos %s" % (letter, currentWord, i))
                    score = 2
                    break
                # check for dupe letters
                elif len(guessPos) == 1 and word[i] != currentWord[num]:
                    adminPrint("%s found but not at pos %s (no dupes)" % (letter, i))
                    score = 1
                    break
                # checks if letter exists in word but in different pos when theres only 1 in word
                elif len(guessPos) > 1 and word[i] != currentWord[num]:
                    adminPrint("%s found but not at pos %s (dupes)" % (letter, i))
                    score = 0
                    break
                else:
                    score = 1
        list.append(score)
        letterCheck(word, score)
    return [list, word]


# letter check
def letterCheck(word, score):
    for i in word:
        letters.update({i: score[word.find(i)]})
    adminPrint("letters updated %s" % letters)


# function to win the game
def winGame(scores):  # TODO make this
    print("\n\nYou Win!\n%s/6 guesses." % len(scores))
    for i in scores:
        print(emojiPrint(i[0]), i[1].upper())


# function to lose the game
def loseGame(scores):  # TODO make this
    print("\n\nYou Lose.\nX/6 guesses.")
    for i in scores:
        print(emojiPrint(i[0]), i[1].upper())
    print("\nThe correct word was %s." % currentWord)


# main
def main():
    while True:
        initGame()
        guessWord()


main()


input("\n\npause debugger :)")
