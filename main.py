from src.core.database import init_db
from src.core.indexer import index_folder
from src.core.paths import get_user_folders
from src.assistant import ask

def build_index():
    init_db()
    folders = get_user_folders()
    for f in folders:
        print(f"Indexation de {f}")
        index_folder(f)
    print("Index terminé.")

def main():
    print("1 - Construire l'index")
    print("2 - Recherche")

    choice = input("> ")

    if choice == "1":
        build_index()
    elif choice == "2":
        while True:
            q = input("Recherche: ")
            print(ask(q))

if __name__ == "__main__":
    main()