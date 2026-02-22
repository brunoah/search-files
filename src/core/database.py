import sqlite3
from pathlib import Path

# Racine du projet : .../search-files
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "index" / "files.db"

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db() -> None:
    conn = get_connection()
    c = conn.cursor()

    # Table principale
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

    # Index utiles
    c.execute("CREATE INDEX IF NOT EXISTS idx_files_ext ON files(ext)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_files_mtime ON files(mtime)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_files_size ON files(size)")

    # FTS5 lié à files (contenu externe)
    c.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS files_fts
    USING fts5(
        name,
        path,
        content='files',
        content_rowid='id'
    )
    """)

    conn.commit()
    conn.close()