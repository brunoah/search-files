from __future__ import annotations
import time
from src.core.search import search_files
from src.llm.parser import parse_query

def _human_size(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    f = float(n)
    for u in units:
        if f < 1024:
            return f"{f:.1f}{u}"
        f /= 1024
    return f"{f:.1f}PB"

def _human_date(ts: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))

def ask(user_text: str) -> str:
    q = parse_query(user_text)
    results = search_files(q)

    if not results:
        return "Aucun résultat."

    lines = []
    lines.append(f"Requête interprétée: sort={q.sort}, ext={q.ext}, recent_days={q.recent_days}, min_size_mb={q.min_size_mb}, text='{q.text}'")
    lines.append("")

    for path, size, mtime, rank in results:
        meta = f"{_human_size(int(size))} | {_human_date(float(mtime))}"
        if rank is not None:
            meta += f" | score={float(rank):.2f}"
        lines.append(f"- {path}\n  {meta}")

    return "\n".join(lines)