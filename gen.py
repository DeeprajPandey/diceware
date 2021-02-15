# gen.py
# Diceware password generator.
#
# Deepraj Pandey
# 14 Feb, 2021

from collections import OrderedDict
from pyperclip import copy, paste
from secrets import randbelow
from subprocess import run
from time import sleep

# Take length of password to be generated (phrase_len)
# TODO: set up argparse with flags and help menu
phrase_len = 5

# Roll dice 5x and generate index code - `phrase_len` times
# randbelow(n) [0,n), hence +1. We need 5 random numbers joined to
# create one index, and `phrase_len` such indices
indices = [("".join([str(randbelow(6) + 1) for _ in range(5)]))
           for _ in range(phrase_len)]

# Ordered Dict of the indices in original random order for storing words
search_space = OrderedDict((i, '') for i in indices)

# Sort for access in one pass of wordlist
# There is probably a beter way to do this.
indices.sort()

# Index into wordlist and get word
filename = "./word.list"
with open(filename, 'r') as f:
    for line in f:
        # if no indices to search for, break
        if not len(indices):
            break

        contents = line.split()
        if contents[0] == indices[0]:
            # place the word in `search_space`
            search_space[indices[0]] = contents[1]
            # indices is sorted, so continuing from next line works
            indices.pop(0)

# Copy passphrase to clipboard
copy("-".join([search_space[id] for id in search_space]))

# Clear clipboard (on MacOS) if it still has the passphrase
# 5 seconds afer pasting
sleep(5)
# Since there is no copy of the password, we check for number of '-'
if paste().count('-') == phrase_len - 1:
    with open("/dev/null", 'r') as nulltext:
        run("pbcopy", stdin=nulltext)
