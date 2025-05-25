#!/usr/bin/env python3
# main.py
"""
By Jmon ft Copilot
Main Program
Calls modular functions to complete the task at hand.
Starts by importing what is needed, sets up logging function, calls generation of
a batch of permutations against set rules to use as 24word mnemonic seed phrases,
then generates the private keys and a wallet address from each seed phrase, then
concatenates a batch of 350 wallet addresses in URI ready format to plug into 
our blockchain_api call. Then calls the batch to the api for checking, checks 
the return status, then parses the relevant data from the api response. Logs all
data along the way as directed, processes final return data, if balance found,
execution is paused and prompts user input, else continues to next batch.
"""

import time
import logging
from logger_setup import setup_logger
from mnemonic_generator import generate_mnemonics
from wallet_gen import generate_wallet_address
from blockchain_api import query_batch_wallet_balances
from progress_tracker import init_db, insert_records, get_start_index
from config import SUB_BATCH_SIZE, BATCH_CANDIDATES, PROXY_CERT, PROXY_CONFIG

def main():
    setup_logger()
    logging.info("Starting AllCoins Puzzle Wallet Checker")
    
    conn = init_db()
    start_index = get_start_index(conn)
    logging.info(f"Resuming from candidate index: {start_index}")

    candidate_counter = 0
    batch_processed = 0
    total_requests = 0
    sub_batch = []

    mnemonic_generator = generate_mnemonics()
    for index, mnemonic in mnemonic_generator:
        if index < start_index:
            continue
        wallet_address = generate_wallet_address(mnemonic)
        if wallet_address is None:
            logging.error(f"Candidate {index}: Wallet generation failed, skipping.")
            continue

        candidate_record = {
            "candidate_index": index,
            "mnemonic": " ".join(mnemonic),
            "wallet_address": wallet_address,
            "final_balance": None,
        }
        sub_batch.append(candidate_record)
        candidate_counter += 1
        batch_processed += 1

        if len(sub_batch) >= SUB_BATCH_SIZE:
            processed_candidates = query_batch_wallet_balances(sub_batch, PROXY_CERT if PROXY_CERT else True, PROXY_CONFIG)
            total_requests += 1
            insert_records(conn, processed_candidates)
            for cand in processed_candidates:
                logging.info(f"Candidate {cand['candidate_index']} | Address: {cand['wallet_address']} | Balance: {cand['final_balance']}")
            sub_batch = []
            if total_requests % 5 == 0:
                logging.info(f"Rate limiting pause for {5} requests, sleeping for 2 seconds")
                time.sleep(2)

        if batch_processed >= BATCH_CANDIDATES:
            logging.info(f"Processed {BATCH_CANDIDATES} candidates. Checkpointing progress at index {index}.")
            user_input = input("Enter 'c' to continue with the next batch or any key to stop: ").strip().lower()
            if user_input != "c":
                break
            batch_processed = 0

    # Process any remaining candidates
    if sub_batch:
        processed_candidates = query_batch_wallet_balances(sub_batch, PROXY_CERT if PROXY_CERT else True, PROXY_CONFIG)
        insert_records(conn, processed_candidates)
        for cand in processed_candidates:
            logging.info(f"Candidate {cand['candidate_index']} | Address: {cand['wallet_address']} | Balance: {cand['final_balance']}")

    logging.info("Processing finished.")
    conn.close()

if __name__ == "__main__":
    main()
