import sqlite3
from pathlib import Path

# CHemin pour la base SQLite
DB_PATH = Path("index/files.db")

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        path TEXT UNIQUE,
        name TEXT,
        ext TEXT,
        size INTEGER,
        mtime REAL
    )
    """)

    # Table FTS pour recherche rapide
    c.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS files_fts
    USING fts5(name, path)
    """)

    conn.commit()
    conn.close()