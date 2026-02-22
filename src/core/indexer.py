import os
from pathlib import Path
from .database import get_connection

def index_folder(folder: Path):
    conn = get_connection()
    c = conn.cursor()

    for root, dirs, files in os.walk(folder):
        for fname in files:
            path = Path(root) / fname

            try:
                stat = path.stat()
            except:
                continue

            ext = path.suffix.lower().lstrip(".")

            try:
                c.execute("""
                INSERT OR IGNORE INTO files(path, name, ext, size, mtime)
                VALUES (?, ?, ?, ?, ?)
                """, (str(path), fname, ext, stat.st_size, stat.st_mtime))

                c.execute("""
                INSERT OR IGNORE INTO files_fts(name, path)
                VALUES (?, ?)
                """, (fname, str(path)))

            except:
                continue

    conn.commit()
    conn.close()