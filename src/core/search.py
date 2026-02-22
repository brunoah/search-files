from __future__ import annotations
import time
from .database import get_connection
from .query import SearchQuery

def _norm_ext(ext: str | None) -> str | None:
    if not ext:
        return None
    ext = str(ext).strip().lower()
    return ext[1:] if ext.startswith(".") else ext

def _clamp_limit(n: int) -> int:
    n = int(n)
    return max(1, min(n, 200))

def search_files(q: SearchQuery):
    """
    Retour: list[(path, size, mtime, rank)]
    rank = bm25(files_fts) si FTS, sinon None
    """
    q.ext = _norm_ext(q.ext)
    q.limit = _clamp_limit(q.limit)
    now = time.time()

    conn = get_connection()
    c = conn.cursor()

    use_fts = bool(q.text and q.text.strip())

    if use_fts:
        # bm25() existe sur FTS5
        base = """
        SELECT f.path, f.size, f.mtime, bm25(files_fts) AS r
        FROM files_fts
        JOIN files f ON files_fts.rowid = f.id
        WHERE files_fts MATCH ?
        """
        params = [q.text.strip()]
    else:
        base = """
        SELECT f.path, f.size, f.mtime, NULL AS r
        FROM files f
        WHERE 1=1
        """
        params = []

    if q.ext:
        base += " AND f.ext = ?"
        params.append(q.ext)

    if q.contains:
        base += " AND f.name LIKE ?"
        params.append(f"%{q.contains}%")

    if q.recent_days is not None:
        min_ts = now - (q.recent_days * 86400)
        base += " AND f.mtime >= ?"
        params.append(min_ts)

    if q.min_size_mb is not None:
        min_bytes = int(q.min_size_mb * 1024 * 1024)
        base += " AND f.size >= ?"
        params.append(min_bytes)

    # Tri
    if q.sort == "relevance" and use_fts:
        base += " ORDER BY r ASC"  # bm25 plus petit = meilleur
    elif q.sort == "mtime_desc":
        base += " ORDER BY f.mtime DESC"
    elif q.sort == "mtime_asc":
        base += " ORDER BY f.mtime ASC"
    elif q.sort == "size_desc":
        base += " ORDER BY f.size DESC"
    elif q.sort == "size_asc":
        base += " ORDER BY f.size ASC"
    elif q.sort == "name_asc":
        base += " ORDER BY f.name ASC"
    else:
        # HYBRID: si FTS -> combine relevance + recency, sinon mtime_desc
        if use_fts:
            # On garde d’abord la pertinence, puis récence
            base += " ORDER BY r ASC, f.mtime DESC"
        else:
            base += " ORDER BY f.mtime DESC"

    base += " LIMIT ?"
    params.append(q.limit)

    c.execute(base, params)
    results = c.fetchall()
    conn.close()
    return results