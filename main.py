from random import randrange
from re import finditer
from csv import reader
from pyperclip import copy

# TODO add docstrings to all functions
# TODO add comments
# TODO add web app for UI

# create wordlist from file
with open("data\\data.csv") as file:
    read = reader(file)
    for i in read:
        WORD_LIST = i


# admin test vars
ENABLE_ADMIN_WORD = False
ADMIN_WORD = "ahhhh"
ENABLE_ADMIN_PRINTS = False
ENABLE_EMOJI_PRINTS = True


# function to print if admin prints are enabled
def adminPrint(data):
    """Print data when ENABLE_ADMIN_PRINTS is True

    Args:
        data (any): any data to get printed
    """
    if ENABLE_ADMIN_PRINTS:
        print(data)


def emojiPrint(list):
    """function to return scores as emojis
    returns string of emojis if ENABLE_EMOJI_PRINTS == True
    returns list if False

    Args:
        list list[int]: list of integers equal to either 0, 1, 2, or -1
    """
    if ENABLE_EMOJI_PRINTS:
        # in theory its impossible for a -1 to be given but it was during testing so im leaving it here
        emojis = ["⬛", "🟨", "🟩", "❌"]
        string = ""
        for i in list:
            string += emojis[i]
        return(string)
    else:
        return(list)


# pick word from answer list
def generateWord():
    """Returns random word from WORD_LIST
    """
    return(WORD_LIST[randrange(0, len(WORD_LIST) - 1)])


# initialise game stuff idk yet
def initGame():
    """Ititialises letters dict, and generates currentWord
    """
    # globals
    global letters
    global currentWord
    letters = {'a': -1, 'b': -1, 'c': -1, 'd': -1, 'e': -1, 'f': -1, 'g': -1, 'h': -1, 'i': -1, 'j': -1, 'k': -1, 'l': -1, 'm': -1,
               'n': -1, 'o': -1, 'p': -1, 'q': -1, 'r': -1, 's': -1, 't': -1, 'u': -1, 'v': -1, 'w': -1, 'x': -1, 'y': -1, 'z': -1}
    if not ENABLE_ADMIN_WORD:
        currentWord = generateWord()
        adminPrint("#############  CURRENT WORD - %s  #############" % currentWord.upper())
    else:
        currentWord = ADMIN_WORD
        adminPrint("#############  ADMIN WORD - %s  #############" % ADMIN_WORD.upper())


# user guessing
def guessWord():
    """Runs the main game
    """
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
                validLetters = []
                for i in "abcdefghijklmnopqrstuvwxyz":
                    if letters[i] == -1:
                        unusedLetters.append(i.upper())
                    elif letters[i] > 0:
                        validLetters.append(i.upper())
                print("Unused letters -\n %s" % str(unusedLetters)[1:-1])
                print("Valid letters  -\n %s" % (str(validLetters)[1:-1]))

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
    saveScore(scores, win)


def wordCheck(word):
    """Function to check letter pos in word in reference to currentWord.

    Args:
        word (str): 5 letter string

    Returns:
        list[ list[int], str ]: 2d list contains, list which contains 5 ints, 5 char string
    """
    list = [-1] * 5

    list = greyCheck(word, list)

    list = greenCheck(word, list)

    list = yellowCheck(word, list)

    return [list, word]


# grey check
def greyCheck(word, list):
    """checks if and letters in word are in currentWord

    Args:
        word (str): 5 letter string
        list (list[int]): list of 5 integers

    Returns:
        list[int]: list of 5 integers
    """
    adminPrint("###### grey check ###### %s" % list)
    for i in range(len(word)):
        adminPrint(" word[i] : %s \n currentWord %s" % (word[i], currentWord))
        if word[i] not in currentWord:
            list[i] = 0
            updateLetter(word, i, 0)
    return list


# green check
def greenCheck(word, list):
    """checks if any letters in word are in the same position in currentWord

    Args:
        word (str): 5 letter string
        list (list[int]): list of 5 integers

    Returns:
        list[int]: list of 5 integers
    """
    adminPrint("###### green check ###### %s" % list)
    for i in range(len(word)):
        if list[i] == -1:
            adminPrint(" word[i] :  %s \n currentWord[i] : %s \n" % (word[i], currentWord[i]))
            if word[i] == currentWord[i]:
                list[i] = 2
                updateLetter(word, i, 2)
    return list


# yellow check
def yellowCheck(word, list):
    """checks to see if letters in word are in currentWord, but not in the exact position. \n
    and also some other checks to make sure the right amount of yellows are in the word. \n
    its confusing just play the game with dupe letters and you might figure it out

    Args:
        word (str): 5 letter string
        list (list[int]): list of 5 integers

    Returns:
        list[int]: list of 5 integers
    """
    adminPrint("###### yellow check ######\n %s" % list)
    for i in range(len(word)):
        if list[i] == -1:

            winPos = [char.start() for char in finditer(word[i], currentWord)]
            guessPos = [char.start() for char in finditer(word[i], word)]
            adminPrint("\n win pos : %s \n guess pos : %s" % (winPos, guessPos))
            adminPrint(" word[i] : %s \n currentWord[i] %s \n i : %s \n" % (word[i], currentWord[i], i))

            if len(guessPos) > 1:
                adminPrint("parse")
                if len(winPos) == 1:
                    if letters[word[i]] == 2:
                        list[i] = 0
                        updateLetter(word, i, 0)
                    else:
                        for j in range(len(guessPos)):
                            if j == 0:
                                value = 1
                            else:
                                value = 0
                            list[guessPos[j]] = value
                            updateLetter(word, guessPos[j], value)
                elif len(guessPos) <= len(winPos):
                    list[i] = 1
                elif len(guessPos) > len(winPos):
                    x = len(guessPos) - len(winPos)
                    for j in range(x):
                        list[j] = 1
                else:
                    list[i] = 0
            else:
                list[i] = 1
                updateLetter(word, i, 1)
                adminPrint("list[i] = 1")
    return list


# letter update
def updateLetter(word, pos, value):
    """updates entry word[pos] in letter dict with value

    Args:
        word (str): 5 letter string
        pos (int): integer referring to a position in word
        value (int): integer value to change to
    """
    adminPrint("\n value : %s \n word[pos] : %s \n" % (value, word[pos]))
    if value > letters[word[pos]]:
        letters.update({word[pos]: value})
        adminPrint("letter %s updated. \n " % (word[pos]))
    else:
        adminPrint("letter %s not updated.\n" % (word[pos]))


# function to win the game
def winGame(scores):
    """outputs score when user wins

    Args:
        scores (list[list[int], str]): 2d list contains, list which contains 5 ints, 5 char string
    """
    print("\n\nYou Win!\n%s/6 guesses." % len(scores))
    share = "Worble %s/6" % len(scores)
    for i in scores:
        print("%s %s" % (emojiPrint(i[0]), i[1].upper()))
        share += "\n%s %s" % (emojiPrint(i[0]), i[1].upper())
    copy(share)


# function to lose the game
def loseGame(scores):
    """outputs score when user loses

    Args:
        scores (list[list[int], str]): 2d list contains, list which contains 5 ints, 5 char string
    """
    print("\n\nYou Lose.\nX/6 guesses.")
    share = "Worble X/6"
    for i in scores:
        print("%s %s" % (emojiPrint(i[0]), i[1].upper()))
        share += "\n%s %s" % (emojiPrint(i[0]), i[1].upper())
    share += "\nThe correct word was %s." % currentWord.upper()
    copy(share)
    print("\nThe correct word was %s." % currentWord.upper())


def saveScore(data, win):
    """write game scores to file

    Args:
        data (list[list[int], str]): 2d list contains, list which contains 5 ints, 5 char string
        win (bool): boolean refering to win/lose
    """
    with (open("scores.txt", "a") as file):
        fileWrite = ""
        for i in data:
            fileWrite += str(i[0])[1:-1]
            fileWrite += " | %s" % i[1]
            fileWrite += "\n"
        if not win:
            x = "X"
        else:
            x = len(data)
        fileWrite += "\n%s %s/6\n---------------------\n" % (currentWord.upper(), x)
        file.write(str(fileWrite))


# main
def main():
    while True:
        initGame()
        guessWord()


main()


input("\n\npause debugger :)")
