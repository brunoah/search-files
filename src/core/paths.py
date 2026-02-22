from pathlib import Path

def get_user_folders() -> list[Path]:
    home = Path.home()
    folders = []

    # Récupération des dossiers à scanner
    for name in ["Documents", "Downloads", "Desktop"]:
        p = home / name
        if p.exists():
            folders.append(p)

    return folders