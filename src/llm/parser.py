from __future__ import annotations
import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from src.core.query import SearchQuery

load_dotenv()

BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
API_KEY = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
MODEL = os.getenv("LMSTUDIO_MODEL", "local-model")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

SYSTEM = """
Tu es un assistant de recherche de fichiers Windows.
Tu dois produire UNIQUEMENT un JSON valide (sans texte autour).

Schéma:
{
  "text": "requête FTS5 MATCH" ou "",
  "ext": "pdf" ou null,
  "contains": "mot" ou null,
  "limit": 20,
  "sort": "hybrid" | "relevance" | "mtime_desc" | "mtime_asc" | "size_desc" | "size_asc" | "name_asc",
  "recent_days": 7 ou null,
  "min_size_mb": 50 ou null
}

Règles:
- Si l'utilisateur dit "pdf" => ext="pdf"
- Si l'utilisateur dit "récent / derniers / cette semaine" => recent_days=7
- Si l'utilisateur dit "aujourd'hui" => recent_days=1
- Si l'utilisateur dit "ce mois" => recent_days=30
- Si l'utilisateur dit "gros / lourds / plus gros" => sort="size_desc"
- Si l'utilisateur dit "les plus gros" => sort="size_desc"
- Si l'utilisateur donne des mots clés libres => text="mots" (FTS)
- Si tu ne sais pas => sort="hybrid", limit=20
"""

def _safe_json_extract(s: str) -> dict:
    s = s.strip().strip("`")
    # Essai 1: JSON direct
    try:
        return json.loads(s)
    except Exception:
        pass
    # Essai 2: extraire le premier bloc {...}
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if m:
        return json.loads(m.group(0))
    raise ValueError("Réponse LLM non JSON")

def parse_query(user_text: str) -> SearchQuery:
    # Fallback “sans IA” (si LM Studio pas chargé / erreur)
    def fallback() -> SearchQuery:
        t = user_text.lower()
        q = SearchQuery()

        # ext
        if "pdf" in t:
            q.ext = "pdf"

        # récence
        if any(k in t for k in ["aujourd", "today"]):
            q.recent_days = 1
        elif any(k in t for k in ["semaine", "7 jours", "derniers"]):
            q.recent_days = 7
        elif "ce mois" in t or "30 jours" in t:
            q.recent_days = 30

        # tri
        if any(k in t for k in ["plus gros", "gros", "lourds"]):
            q.sort = "size_desc"

        # texte FTS simple: on enlève quelques mots “bruit”
        noise = {"montre", "moi", "les", "des", "du", "de", "d'", "fichiers", "file", "sur", "mon", "ordi"}
        tokens = [w for w in re.findall(r"[a-zA-Z0-9_]+", t) if w not in noise]
        q.text = " ".join(tokens[:6])
        return q

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user_text},
            ],
            temperature=0.2,
        )
        content = resp.choices[0].message.content or ""
        data = _safe_json_extract(content)

        q = SearchQuery(
            text=str(data.get("text") or "").strip(),
            ext=data.get("ext"),
            contains=data.get("contains"),
            limit=int(data.get("limit") or 20),
            sort=str(data.get("sort") or "hybrid"),
            recent_days=data.get("recent_days"),
            min_size_mb=data.get("min_size_mb"),
        )
        return q
    except Exception:
        return fallback()