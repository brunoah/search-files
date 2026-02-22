from src.core.search import search_files
from src.llm.parser import parse_query

def ask(user_text: str):
    data = parse_query(user_text)

    results = search_files(
        ext=data.get("ext"),
        contains=data.get("contains"),
        limit=data.get("limit", 20)
    )

    if not results:
        return "Aucun résultat."

    output = ""
    for path, size, mtime in results:
        output += f"{path}\n"

    return output