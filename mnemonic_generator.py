#!/usr/bin/env python3
"""
By Jmon ft. Copilot
Module Function for creating permutations of possible seed phrases to be 
generated into BTC wallet keys. This code reflects the conditions that exist 
for the Puzzle Wallet challenge that this code was designed for. It accounts for
the 6-word prefix of words in position that were given as definitely correct,
it accounts for the 2 words we know are definitely in which for each we know one 
7 positions each definitely does NOT go (6 for the prefix and 1 other positions).
"""

# mnemonic_generator.py

import itertools
from config import PREFIX, FREE_WORDS, GROUP2_WORDS, TOTAL_WORDS, FIRST_BLOCK_COUNT
import logging

def generate_mnemonics():
    """
    Yields tuples of (index, mnemonic) where mnemonic is a list of 24 words following the rules.
    """
    index = 0
    for first_block in itertools.permutations(FREE_WORDS, FIRST_BLOCK_COUNT):
        if first_block[0] == "bridge" or first_block[1] == "current":
            continue
        free_remaining = [word for word in FREE_WORDS if word not in first_block]
        second_block_pool = GROUP2_WORDS + free_remaining
        if len(second_block_pool) != 12:
            logging.error("Unexpected pool size for second block (should be 12).")
            continue
        for second_block in itertools.permutations(second_block_pool, 12):
            mnemonic = PREFIX + list(first_block) + list(second_block)
            if len(mnemonic) != TOTAL_WORDS:
                continue
            yield index, mnemonic
            index += 1
