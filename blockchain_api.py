#!/usr/bin/env python3
# blockchain_api.py
"""
By Jmon ft Copilot
Module for making the BTC wallet balance check call to the Blockchain API
Utilizing Blockchain.com's blockchain.info request API. After comparing several
API's to serve this function, blockchain.info is by far the best option. Not only
does it have the highest tolerance for high frequency requesting, it allows batch
requests for as many wallet addresses you can fit within the maximum URI legnth
limit (350>500~), is it totally free to use, and to top it off like that wasn't
already amazing, it does not even require an API key... My original code for 
this purpose used to hammer this api with requests for hours at a time and never
once was I denied, banned, or rate-limited.
"""

import requests
import time
import logging
from config import (
    BALANCE_URL_TEMPLATE, MAX_REQUEST_ATTEMPTS, RETRY_POINT_LIMIT,
    CRITICAL_STATUS_CODES, TIMEOUT_SECONDS
)

def query_batch_wallet_balances(candidates, verify_cert, proxy_config):
    """
    Given a list of candidate records, batch query the blockchain API.
    """
    addresses = [cand["wallet_address"] for cand in candidates]
    joined_addresses = "|".join(addresses)
    url = BALANCE_URL_TEMPLATE.format(wallet_addr=joined_addresses)
    points = 0
    attempts = 0
    while attempts < MAX_REQUEST_ATTEMPTS and points < RETRY_POINT_LIMIT:
        try:
            response = requests.get(url, proxies=proxy_config, verify=verify_cert, timeout=TIMEOUT_SECONDS)
            status = response.status_code
            logging.debug(f"Batch Request URL: {url} | Status Code: {status}")
        except requests.RequestException as e:
            logging.error(f"RequestException in batch query: {e}")
            points += 1
            attempts += 1
            time.sleep(1)
            continue

        if status == 200:
            try:
                data = response.json()
                for cand in candidates:
                    addr = cand["wallet_address"]
                    addr_data = data.get(addr, {})
                    if isinstance(addr_data, dict):
                        cand["final_balance"] = addr_data.get("final_balance", 0)
                    else:
                        logging.error(f"Unexpected data format for address {addr}: {addr_data}")
                        cand["final_balance"] = 0
                return candidates
            except Exception as e:
                logging.error(f"Error parsing batch JSON: {e}")
                points += 1
        else:
            if status in CRITICAL_STATUS_CODES:
                logging.warning(f"Critical status code {status} received. Aborting retries for this batch.")
                points += 5
            else:
                points += 1
            logging.warning(f"Non-200 status code {status}. Attempt {attempts + 1} of {MAX_REQUEST_ATTEMPTS}.")
        attempts += 1
        time.sleep(1)
    logging.error("Failed to obtain batch balance data after retries.")
    for cand in candidates:
        cand["final_balance"] = None
    return candidates
