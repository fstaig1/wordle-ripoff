import random as r


WORD_FREQ_FILE = "wordle-ripoff\\data\\word freq.txt"
WORD_FILE = "wordle-ripoff\\data\\words.txt"
ANSWER_FILE = "wordle-ripoff\\data\\answers.txt"
ANSWER_FREQ_FILE = "wordle-ripoff\\data\\answer freq.txt"
WORD_FREQ_LIST = []
WORD_LIST = []
ANSWER_LIST = []
ANSWER_FREQ_LIST = []
with(open(WORD_FREQ_FILE) as file):
    for line in file:
        WORD_FREQ_LIST.append(line.split("\n")[0].split(" "))
        WORD_LIST.append(line.split("\n")[0].split(" ")[0])


with(open(ANSWER_FREQ_FILE) as file):
    for line in file:
        ANSWER_FREQ_LIST.append(line.split("\n")[0].split(" "))
        ANSWER_LIST.append(line.split("\n")[0].split(" ")[0])


def chooseWord():
    return(ANSWER_LIST[r.randrange(0,len(ANSWER_LIST)-1)])


def initGame():
    currentWord = chooseWord()
    return currentWord
    
    
def main():
    initGame()
    
    print("pause debugger :)")

main()