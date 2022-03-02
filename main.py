from random import randrange
from re import finditer
from csv import reader
from pyperclip import copy

# TODO add docstrings to all functions

# constants
with open("data\\data.csv") as file:
    read = reader(file)
    for i in read:
        WORD_LIST = i


# admin test vars
ENABLE_ADMIN_WORD = True
ADMIN_WORD = "ahhhh"
ENABLE_ADMIN_PRINTS = True
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
    saveScore(scores, win)


def wordCheck(word):
    """Function to check letter pos in word in reference to currentWord.

    Args:
        word (str): 5 letter string

    Returns:
        list[ list[int], str ]: 2d list contains, list which contains 5 ints, 5 char string
    """
    list = [-1] * 5
    
    # grey check
    adminPrint("###### grey check ###### %s" % list)
    for i in range(len(word)):
        adminPrint("word[i] %s : currentWord %s" % (word[i], currentWord))
        if word[i] not in currentWord:
            adminPrint("parse")
            list[i] = 0
            letterCheck(word, i, 0)
    
    # green check
    adminPrint("###### green check ###### %s" % list)
    for i in range(len(word)):
        if list[i] == -1:
            adminPrint(" word[i] %s \n currentWord[i] %s \n" % (word[i], currentWord[i]))
            if word[i] == currentWord[i]:
                list[i] = 2
                letterCheck(word, i, 2)
        else: 
            continue
    
    # yellow check
    adminPrint("###### yellow check ######\n %s" % list)
    for i in range(len(word)):
        if list[i] == -1:
            
            winPos = [char.start() for char in finditer(word[i], currentWord)]
            guessPos = [char.start() for char in finditer(word[i], word)]
            tempGuessPos = guessPos
            adminPrint("\n win pos %s \n guess pos%s" % (winPos, guessPos))
            adminPrint(" word[i] %s \n currentWord[i] %s \n i %s \n" % (word[i], currentWord[i], i))
            
            if len(guessPos) > 1:
                adminPrint("parse")
                if letters[word[i]] == 2:
                    list[i] = 0
                else:
                    for i in range(len(guessPos)):
                        if i == 0:
                            value = 1
                        else:
                            value = 0
                        list[guessPos[i]] = value
                    
            else:
                list[i] = 1
                adminPrint("list[i] = 1")
        else:
            continue
    
    for i in list:
        if i == -1:
            i = 0
        
    
    
    return [list, word]


# letter check
def letterCheck(word, pos, value):
    
    if value > letters[word[pos]]:
        letters.update({word[pos]: value})
    adminPrint("letter %s updated. \n " % (word[pos]))


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
    share += "\nThe correct word was %s." % currentWord
    copy(share)
    print("\nThe correct word was %s." % currentWord)


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
        fileWrite += "\n%s %s/6\n---------------------\n" % (currentWord, x)
        file.write(str(fileWrite))


# main
def main():
    while True:
        initGame()
        guessWord()


main()


input("\n\npause debugger :)")
