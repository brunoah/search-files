# 🔎 search-files

> Assistant IA local de recherche de fichiers\
> Indexation persistante, recherche FTS5, tri intelligent et API locale.

------------------------------------------------------------------------

## 🚀 Présentation

**search-files** est un moteur de recherche de fichiers local développé
en Python, combinant :

-   ⚡ Indexation persistante via SQLite
-   🔎 Recherche ultra-rapide avec FTS5
-   🤖 Interprétation en langage naturel via LM Studio
-   🧠 Tri intelligent (pertinence, date, taille, hybride)
-   🔄 Indexation incrémentale
-   🌐 API locale FastAPI

Le projet est conçu comme une brique d'infrastructure pour assistants IA
locaux (ex : intégration future avec FRANK).

------------------------------------------------------------------------

## 🧠 Fonctionnalités V2

### 🔹 Indexation intelligente

-   Scan des dossiers utilisateur :
    -   Documents
    -   Téléchargements
    -   Bureau
-   Stockage des métadonnées :
    -   Chemin complet
    -   Nom
    -   Extension
    -   Taille
    -   Date de modification
-   Mise à jour incrémentale

### 🔹 Recherche avancée

-   Recherche FTS5 (`MATCH`)
-   Support AND / OR / phrase exacte
-   Classement par pertinence (BM25)
-   Tri par :
    -   Pertinence
    -   Date (asc/desc)
    -   Taille (asc/desc)
    -   Nom
    -   Hybride (pertinence + récence)

### 🔹 Analyse IA

Requête utilisateur → LLM → JSON structuré :

``` json
{
  "text": "facture pdf",
  "ext": "pdf",
  "limit": 20,
  "sort": "hybrid",
  "recent_days": 30
}
```

Fallback automatique si le LLM ne renvoie pas un JSON valide.

------------------------------------------------------------------------

## 🏗 Architecture

    search-files/
    │
    ├── index/
    │   └── files.db
    │
    ├── src/
    │   ├── core/
    │   │   ├── database.py
    │   │   ├── indexer.py
    │   │   ├── search.py
    │   │   ├── query.py
    │   │   └── paths.py
    │   │
    │   ├── llm/
    │   │   └── parser.py
    │   │
    │   ├── api/
    │   │   └── app.py
    │   │
    │   └── assistant.py
    │
    └── main.py

------------------------------------------------------------------------

## ⚙️ Prérequis

-   Python 3.10+
-   LM Studio
-   Modèle LLM chargé (Mistral, Qwen, etc.)
-   Windows 10/11

------------------------------------------------------------------------

## 🔧 Installation

### 1️⃣ Cloner le projet

    git clone https://github.com/brunoah/search-files.git
    cd search-files

### 2️⃣ Environnement virtuel

    python -m venv .venv
    .venv\Scripts\activate

### 3️⃣ Installer les dépendances

    pip install -r requirements.txt

------------------------------------------------------------------------

## 🧠 Configuration LM Studio

1.  Activer l'API OpenAI compatible\
2.  Charger un modèle\
3.  Vérifier :

```{=html}
<!-- -->
```
    http://localhost:1234/v1/models

Créer un fichier `.env` :

    LMSTUDIO_BASE_URL=http://localhost:1234/v1
    LMSTUDIO_API_KEY=lm-studio
    LMSTUDIO_MODEL=nom-du-modele

------------------------------------------------------------------------

## 🏗 Commandes

### 🔹 Rebuild complet

    python main.py build

### 🔹 Update incrémental

    python main.py update

### 🔹 Recherche interactive

    python main.py search

Exemples :

    pdf récents
    les plus gros fichiers
    facture pdf ce mois
    "X56 Template"

### 🔹 Lancer l'API

    python main.py api --port 8005

Endpoints :

-   `GET /health`
-   `POST /search`

``` json
{ "q": "pdf facture récents" }
```

------------------------------------------------------------------------

## 🔐 Confidentialité

-   100% local
-   Aucun upload de fichier
-   Aucun appel API externe
-   LLM exécuté localement

------------------------------------------------------------------------

## 📊 Performance

-   Indexation initiale : dépend du volume
-   Update : rapide et ciblé
-   Recherche : quasi instantanée
-   Optimisations SQLite activées (WAL + index)

------------------------------------------------------------------------

## 🛠 Roadmap

-   [ ] Scoring hybride avancé
-   [ ] Recherche sémantique (embeddings locaux)
-   [ ] Filtrage par dossier intelligent
-   [ ] Interface graphique
-   [ ] Intégration complète FRANK

------------------------------------------------------------------------

## 👨‍💻 Auteur

**Bruno Ahée**\
Développeur de systèmes IA\
Créateur de FRANK Assistant

GitHub : https://github.com/brunoah/search-files

------------------------------------------------------------------------

## 📄 Licence

MIT
