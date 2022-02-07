
from pkg_resources import yield_lines


WORD_FREQ_FILE = "wordle-ripoff\data\word freq.txt"
WORD_FILE = "wordle-ripoff\data\words.txt"
ANSWER_FILE = "wordle-ripoff\\data\\answers.txt"

WORD_FREQ_LIST = []
WORD_LIST = []
ANSWER_LIST = []

with(open(WORD_FREQ_FILE) as file):
    for line in file:
        WORD_FREQ_LIST.append(line.split("\n")[0].split(" "))
        WORD_LIST.append(line.split("\n")[0].split(" ")[0])

with(open(ANSWER_FILE) as file):
    for line in file:
        ANSWER_LIST.append(line)

