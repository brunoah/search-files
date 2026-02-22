from .database import get_connection

def search_files(ext=None, contains=None, limit=20):
    conn = get_connection()
    c = conn.cursor()

    query = "SELECT path, size, mtime FROM files WHERE 1=1"
    params = []

    if ext:
        query += " AND ext = ?"
        params.append(ext)

    if contains:
        query += " AND name LIKE ?"
        params.append(f"%{contains}%")

    query += " ORDER BY mtime DESC LIMIT ?"
    params.append(limit)

    c.execute(query, params)
    results = c.fetchall()

    conn.close()
    return results