import random as r
from os import system
import re


# function to let me easily clear the screen
def clear():
    system("cls")


# constants
WORD_LIST = []
with(open("data\\sgb-words.txt", "r") as file):
    for line in file:
        WORD_LIST.append(line.strip("\n"))
global letters
letters = {'a': -1, 'b': -1, 'c': -1, 'd': -1, 'e': -1, 'f': -1, 'g': -1, 'h': -1, 'i': -1, 'j': -1, 'k': -1, 'l': -1, 'm': -1,
           'n': -1, 'o': -1, 'p': -1, 'q': -1, 'r': -1, 's': -1, 't': -1, 'u': -1, 'v': -1, 'w': -1, 'x': -1, 'y': -1, 'z': -1}


# admin test vars
ENABLE_ADMIN_WORD = True
ADMIN_WORD = "stern"
ENABLE_ADMIN_PRINTS = True
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
    win = False
    for guessNum in range(1, 7):
        valid = False
        while not valid:
            print("\nGuess #%s." % guessNum)
            adminPrint("/ %s /" % generateWord())
            if guessNum > 1:
                for i in scores:
                    print("%s %s" % (emojiPrint(i[0]), i[1].upper()))
                unusedLetters = []
                for i in "abcdefghijklmnopqrstuvwxyz":
                    if letters[i] == -1:
                        unusedLetters.append(i.upper())
                print("Unused letters -\n %s" % str(unusedLetters)[1:-1])
                    
            guess = input("> ").lower()

            if guess in WORD_LIST:
                valid = True
            else:
                print("enter a valid 5 letter word")
        score = wordCheck(word=guess)

        scores.append(score)
        if score[0] == [2, 2, 2, 2, 2]:
            win = True
            break
    if win:
        winGame(scores)
    else:
        loseGame(scores)
    with (open("scores.txt", "a") as file):
        fileWrite = ""
        for i in scores:
            fileWrite += str(i[0])[1:-1]
            fileWrite += " %s" % i[1]
            fileWrite += "\n"
        fileWrite += "\n%s %s/6\n---------------------\n" % (currentWord, len(scores[0]))
        file.write(str(fileWrite))


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
            for i in winPos:
                adminPrint("word[i] %s currentWord[num] %s" % (word[i], currentWord[num]))
                # check if letter in exact pos
                if word[num] == currentWord[num]:
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
    letterCheck(word, list)
    return [list, word]



# letter check
def letterCheck(word, list):
    for i in range(0, len(list)):
        letters.update({word[i] : list[i]})
    adminPrint("letters updated %s" % letters)


# function to win the game
def winGame(scores):  # TODO make this
    print("\n\nYou Win!\n%s/6 guesses." % len(scores))
    for i in scores:
        print("%s %s" % (emojiPrint(i[0]), i[1].upper()))


# function to lose the game
def loseGame(scores):  # TODO make this
    print("\n\nYou Lose.\nX/6 guesses.")
    for i in scores:
        print("%s %s" % (emojiPrint(i[0]), i[1].upper()))
    print("\nThe correct word was %s." % currentWord)


# main
def main():
    while True:
        initGame()
        guessWord()


main()


input("\n\npause debugger :)")
