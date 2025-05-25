#!/usr/bin/env python3
# progress_tracker.py
"""
By Jmon ft Copilot
Essential progress tracking and resume functions to allow for starting and 
stopping without overlaps or unnecessary requests or wasted time. When tackling
an astronomical task such as this, this fuctionality is a must. 
"""

import sqlite3
import logging
from config import DB_FILE

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        candidate_index INTEGER PRIMARY KEY,
        mnemonic TEXT,
        wallet_address TEXT,
        final_balance INTEGER,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    return conn

def insert_records(conn, records):
    cur = conn.cursor()
    data = [(rec["candidate_index"], rec["mnemonic"], rec["wallet_address"], rec["final_balance"])
            for rec in records]
    cur.executemany("""
        INSERT OR REPLACE INTO progress(candidate_index, mnemonic, wallet_address, final_balance)
        VALUES (?, ?, ?, ?)
    """, data)
    conn.commit()

def get_start_index(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(candidate_index) FROM progress")
    row = cur.fetchone()
    return row[0] + 1 if row and row[0] is not None else 0
