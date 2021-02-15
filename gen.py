# gen.py
# Diceware password generator.
#
# Deepraj Pandey
# 14 Feb, 2021

from secrets import randbelow
from collections import OrderedDict

# Take length of password to be generated (len)
# TODO: set up argparse with flags and help menu
len = 5

# Do len times
# Roll dice 5x and generate index code
# randbelow(n) [0,n), hence +1. We need 5 random numbers joined to
# create one index, and `len` such indices
indices = [("".join([str(randbelow(6) + 1) for _ in range(5)]))
           for _ in range(len)]

# Ordered Dict of the indices in original random order for storing words
search_space = OrderedDict((i, '') for i in indices)

print(search_space.keys())
# Sort for access in one pass of wordlist
# There is probably a beter way to do this.
indices.sort()

# Index into wordlist and get word

# Append to pass
for id in search_space:
    print(id)

# Print passphrase
# TODO: better way? copy to clipboard automatically?
