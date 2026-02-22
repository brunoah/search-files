# 📁 search-files

> Assistant IA local de recherche de fichiers utilisant LM Studio\
> Indexation persistante, recherche rapide et compréhension en langage
> naturel.

------------------------------------------------------------------------

## 🚀 Présentation

**search-files** est un moteur de recherche de fichiers local développé
en Python.

Il combine :

-   ⚡ Indexation persistante via SQLite
-   🔎 Recherche rapide et optimisée
-   🤖 Analyse des requêtes en langage naturel via LM Studio
-   🧠 Transformation intelligente des demandes en requêtes structurées
-   🗂 Indexation ciblée (Documents, Téléchargements, Bureau)

Contrairement à la recherche Windows classique, ce projet permet des
requêtes naturelles comme :

    montre moi les pdf récents
    pdf contenant facture
    documents frank
    plus gros fichiers de ce mois

------------------------------------------------------------------------

## 🏗 Architecture

    search-files/
    │
    ├── index/
    │   └── files.db                # Base SQLite persistante
    │
    ├── src/
    │   ├── core/
    │   │   ├── paths.py            # Détection des dossiers utilisateur
    │   │   ├── database.py         # Initialisation SQLite
    │   │   ├── indexer.py          # Scan et indexation
    │   │   └── search.py           # Exécution des requêtes
    │   │
    │   ├── llm/
    │   │   └── parser.py           # Langage naturel → JSON structuré
    │   │
    │   └── assistant.py            # Orchestration IA
    │
    └── main.py                     # Interface CLI

------------------------------------------------------------------------

## ⚙️ Prérequis

-   Python 3.10+
-   LM Studio
-   Un modèle LLM chargé (Mistral, Qwen, etc.)
-   Windows 10/11

------------------------------------------------------------------------

## 🔧 Installation

### 1️⃣ Cloner le dépôt

    git clone https://github.com/brunoah/search-files.git
    cd search-files

### 2️⃣ Créer l'environnement virtuel

    python -m venv .venv
    .venv\Scripts\activate

### 3️⃣ Installer les dépendances

    pip install -r requirements.txt

Si nécessaire :

    pip install openai python-dotenv

------------------------------------------------------------------------

## 🧠 Configuration LM Studio

1.  Ouvrir LM Studio\
2.  Activer :
    -   ✅ OpenAI compatible API\
    -   ✅ Start server on launch\
3.  Charger un modèle (ex : mistral-7b-instruct)\
4.  Vérifier :

```{=html}
<!-- -->
```
    http://localhost:1234/v1/models

------------------------------------------------------------------------

## 🏗 Construire l'index

Premier lancement :

    python main.py

Choisir :

    1 - Construire l'index

Les dossiers indexés :

-   Documents
-   Téléchargements
-   Bureau

Base générée dans :

    index/files.db

------------------------------------------------------------------------

## 🔎 Recherche

Après indexation :

    python main.py

Choisir :

    2 - Recherche

Exemples :

    pdf
    pdf facture
    documentation frank
    x56 template

------------------------------------------------------------------------

## 🧩 Fonctionnement

### Indexation

-   Scan des dossiers ciblés
-   Stockage des métadonnées :
    -   Chemin
    -   Nom
    -   Extension
    -   Taille
    -   Date de modification
-   Persistance via SQLite

### Analyse IA

Requête utilisateur → LLM → JSON structuré :

    {
      "ext": "pdf",
      "contains": "facture",
      "limit": 20
    }

Puis traduction en requête SQL optimisée.

------------------------------------------------------------------------

## 🔐 Confidentialité

-   Exécution 100% locale
-   Aucun fichier envoyé sur Internet
-   Aucun appel API externe
-   LLM exécuté localement via LM Studio

------------------------------------------------------------------------

## 🛠 Roadmap

-   [ ] Recherche FTS5 avancée
-   [ ] Indexation incrémentale
-   [ ] API locale FastAPI
-   [ ] Recherche sémantique par embeddings
-   [ ] Interface graphique
-   [ ] Intégration avec FRANK

------------------------------------------------------------------------

## 👨‍💻 Auteur

**Bruno Ahée**\
Développeur de systèmes IA\
Créateur de FRANK Assistant

GitHub : https://github.com/brunoah/search-files

------------------------------------------------------------------------

## 📄 Licence

MIT (recommandée)
