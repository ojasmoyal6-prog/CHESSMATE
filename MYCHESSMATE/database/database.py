import sqlite3
import os
import json
from datetime import datetime

DB_PATH = "chessmind.db"

def get_connection():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            rating INTEGER DEFAULT 1200,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            opponent TEXT,
            difficulty TEXT,
            color TEXT,
            result TEXT,
            pgn TEXT,
            accuracy REAL,
            blunders INTEGER,
            mistakes INTEGER,
            opening TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            move_number INTEGER,
            player_move TEXT,
            best_move TEXT,
            eval_before REAL,
            eval_after REAL,
            classification TEXT,
            explanation TEXT,
            FOREIGN KEY(game_id) REFERENCES games(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            category TEXT,
            success BOOLEAN,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()