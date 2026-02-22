import os
from pathlib import Path
from .database import get_connection

SKIP_DIRS = {".git", "node_modules", "__pycache__"}

def _upsert_file(c, path: Path, name: str, ext: str, size: int, mtime: float) -> None:
    # Insert / Update sur la table files
    c.execute("""
    INSERT INTO files(path, name, ext, size, mtime)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(path) DO UPDATE SET
        name=excluded.name,
        ext=excluded.ext,
        size=excluded.size,
        mtime=excluded.mtime
    """, (str(path), name, ext, size, mtime))

    # Sync FTS: on mappe rowid = id
    c.execute("""
    INSERT OR REPLACE INTO files_fts(rowid, name, path)
    SELECT id, name, path FROM files WHERE path = ?
    """, (str(path),))

def build_index(folders: list[Path]) -> tuple[int, int]:
    """
    Reconstruit l'index à partir des dossiers.
    Retourne (nb_fichiers_indexés, nb_erreurs)
    """
    conn = get_connection()
    c = conn.cursor()

    # Nettoyage (rebuild total)
    c.execute("DELETE FROM files")
    c.execute("DELETE FROM files_fts")

    conn.commit()

    indexed = 0
    errors = 0

    for folder in folders:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                p = Path(root) / fname
                try:
                    st = p.stat()
                    ext = p.suffix.lower().lstrip(".")
                    _upsert_file(c, p, p.name, ext, int(st.st_size), float(st.st_mtime))
                    indexed += 1
                except Exception:
                    errors += 1

    conn.commit()
    conn.close()
    return indexed, errors

def update_index(folders: list[Path]) -> tuple[int, int]:
    """
    Update incrémental:
    - upsert fichiers présents
    - supprime les entrées dont le fichier n'existe plus
    Retourne (nb_modifiés/ajoutés, nb_supprimés)
    """
    conn = get_connection()
    c = conn.cursor()

    # Charge l’état existant
    c.execute("SELECT path, mtime, size FROM files")
    existing = {row[0]: (row[1], row[2]) for row in c.fetchall()}

    seen: set[str] = set()
    upserts = 0

    for folder in folders:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                p = Path(root) / fname
                sp = str(p)
                try:
                    st = p.stat()
                    mtime = float(st.st_mtime)
                    size = int(st.st_size)
                    seen.add(sp)

                    old = existing.get(sp)
                    # Upsert si nouveau ou modifié
                    if old is None or old[0] != mtime or old[1] != size:
                        ext = p.suffix.lower().lstrip(".")
                        _upsert_file(c, p, p.name, ext, size, mtime)
                        upserts += 1
                except Exception:
                    continue

    # Supprimer fichiers supprimés
    to_delete = [p for p in existing.keys() if p not in seen]
    deleted = 0
    for p in to_delete:
        c.execute("DELETE FROM files WHERE path = ?", (p,))
        # rowid = id, mais comme on a supprimé files, on supprime aussi par path en FTS
        c.execute("DELETE FROM files_fts WHERE path = ?", (p,))
        deleted += 1

    conn.commit()
    conn.close()
    return upserts, deleted