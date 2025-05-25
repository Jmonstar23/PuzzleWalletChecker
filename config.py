#!/usr/bin/env python3
"""

"""
# config.py

# Fixed prefix words, free words, etc.
PREFIX = ["head", "honey", "bitter", "find", "sock", "dash"]
FREE_WORDS = ["bridge", "current", "tail", "bottom", "matter", "like", "arrive", "addict", "fish", "inch"]
GROUP2_WORDS = ["segway", "allcoins", "crypto", "website", "breath", "fight", "passenger", "gimmick"]
TOTAL_WORDS = 24
FIRST_BLOCK_COUNT = 6

# Batching / API constants
BATCH_CANDIDATES = 350_000
SUB_BATCH_SIZE = 350  # for example, if you want to increase the subbatch size
BALANCE_URL_TEMPLATE = "http://blockchain.info/balance?active={wallet_addr}"
MAX_REQUEST_ATTEMPTS = 5
RETRY_POINT_LIMIT = 5
CRITICAL_STATUS_CODES = {429, 403, 418, 420}
REQUEST_PAUSE_COUNT = 5
REQUEST_PAUSE_SECONDS = 2
TIMEOUT_SECONDS = 30  # request timeout

# Proxy settings
PROXY_CERT = "/Users/macbook/python/charles-ssl-proxying-certificate.pem"
PROXY_CONFIG = {
    "https": "http://127.0.0.1:8888"
#    "http": "http://127.0.0.1:8888",
}
# Uncomment http PROXY_CONFIG if wish to use, move comma from http up to https
# If not using proxy, you can set PROXY_CONFIG = None
# PROXY_CONFIG = None

  
# Database file
DB_FILE = "progress.db"
