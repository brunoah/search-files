from dataclasses import dataclass
from typing import Optional, Literal

SortMode = Literal["hybrid", "relevance", "mtime_desc", "mtime_asc", "size_desc", "size_asc", "name_asc"]

@dataclass
class SearchQuery:
    text: str = ""                 # requête FTS (MATCH)
    ext: Optional[str] = None       # "pdf"
    contains: Optional[str] = None  # fallback LIKE
    limit: int = 20
    sort: SortMode = "hybrid"
    recent_days: Optional[int] = None   # filtre récence
    min_size_mb: Optional[float] = None # filtre gros fichiers (>=)