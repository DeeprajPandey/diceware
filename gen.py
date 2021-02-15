# gen.py
# Diceware password generator.
#
# Uses pyperclip for adding the password to the clipboard which
# depends on xclip on linux (https://pypi.org/project/pyperclip/).
#
# ----
# Security Note from pyperclip's source code
# (https://github.com/asweigart/pyperclip/blob/master/src/pyperclip/__init__.py)
# This module (pyperclip) runs programs with these names:
#     - which
#     - where
#     - pbcopy
#     - pbpaste
#     - xclip
#     - xsel
#     - wl-copy/wl-paste
#     - klipper
#     - qdbus
# A malicious user could rename or add programs with these names, tricking
# Pyperclip into running them with whatever permissions the Python process has.
# ----
#
# Deepraj Pandey
# 14 Feb, 2021

from collections import OrderedDict
from pyperclip import copy, paste
from secrets import randbelow
from shlex import quote
from subprocess import Popen
from time import sleep

# Take length of password to be generated (phrase_len)
# TODO: set up argparse with flags and help menu
phrase_len = 5
clipboard_timeout = 5  # time to wait in seconds before clearing clipboard

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
# `clipboard_timeout` seconds afer pasting.
# Since there is no copy of the password, we check for number of '-'
if paste().count('-') == phrase_len - 1:
    # TODO: check host OS and use respective clipboard command
    # TODO: bash windows users
    cmd = "sleep {} && pbcopy < /dev/null".format(
        quote(str(clipboard_timeout)))
    Popen(cmd, shell=True, start_new_session=True)
