#!/usr/bin/env python3
"""
By Jmon ft. Copilot
Module/Function to set up a logging system for status updates and
debugging functionality for the AllCoin Wallet Cracker script.
"""

# logger_setup.py
import logging

def setup_logger(level=logging.DEBUG, log_file="allcoins.log"):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
