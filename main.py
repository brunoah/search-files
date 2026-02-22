from __future__ import annotations
import argparse
from rich.console import Console
from rich.prompt import Prompt

from src.core.database import init_db
from src.core.paths import get_user_folders
from src.core.indexer import build_index, update_index
from src.assistant import ask

console = Console()

def cmd_build():
    init_db()
    folders = get_user_folders()
    console.print("[bold]Indexation (rebuild total)[/bold]")
    for f in folders:
        console.print(f"- {f}")
    indexed, errors = build_index(folders)
    console.print(f"\n✅ Index terminé: {indexed} fichiers, erreurs={errors}")

def cmd_update():
    init_db()
    folders = get_user_folders()
    console.print("[bold]Indexation (update incrémental)[/bold]")
    for f in folders:
        console.print(f"- {f}")
    upserts, deleted = update_index(folders)
    console.print(f"\n✅ Update terminé: upserts={upserts}, supprimés={deleted}")

def cmd_search():
    init_db()
    console.print("[bold]search-files V2[/bold] — tape 'exit' pour quitter\n")
    while True:
        q = Prompt.ask("Recherche")
        if q.strip().lower() in {"exit", "quit"}:
            break
        console.print("\n[cyan]Résultat[/cyan]")
        console.print(ask(q))
        console.print()

def cmd_api(host: str, port: int):
    import uvicorn
    # Lance l’API FastAPI
    uvicorn.run("src.api.app:app", host=host, port=port, reload=False)

def main():
    parser = argparse.ArgumentParser(prog="search-files")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("build", help="Rebuild complet de l'index")
    sub.add_parser("update", help="Update incrémental de l'index")
    sub.add_parser("search", help="Recherche interactive")

    p_api = sub.add_parser("api", help="Lancer l'API FastAPI")
    p_api.add_argument("--host", default="127.0.0.1")
    p_api.add_argument("--port", type=int, default=8005)

    args = parser.parse_args()

    if args.cmd == "build":
        cmd_build()
    elif args.cmd == "update":
        cmd_update()
    elif args.cmd == "search":
        cmd_search()
    elif args.cmd == "api":
        cmd_api(args.host, args.port)

if __name__ == "__main__":
    main()