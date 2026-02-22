from pathlib import Path

def get_user_folders() -> list[Path]:
    home = Path.home()
    candidates = ["Documents", "Downloads", "Desktop"]
    folders: list[Path] = []
    for name in candidates:
        p = home / name
        if p.exists():
            folders.append(p)
    return folders