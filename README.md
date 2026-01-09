# 📚 Semantic Search API (PDF → Recherche sémantique)

## 🎓 Contexte académique

Ce projet a été réalisé dans le cadre d’un **projet de Master en Data Science / Ingénierie logicielle**. Il vise à implémenter une **API de recherche sémantique moderne** permettant d’indexer des documents PDF et d’effectuer des recherches basées sur le sens, et non sur de simples mots-clés.

---

## 🎯 Objectifs du projet

* Permettre aux utilisateurs d’uploader des **documents PDF**
* Extraire automatiquement le **texte** des PDF
* Découper les documents en **segments (chunks)**
* Générer des **embeddings vectoriels** pour chaque chunk
* Stocker les embeddings dans une **base vectorielle (pgvector)**
* Réaliser une **recherche sémantique** par similarité cosinus
* Proposer des **documents similaires**
* Conserver l’**historique des recherches utilisateur**

---

## 🧠 Architecture générale

```
PDF
 ↓
Extraction du texte
 ↓
Découpage en chunks
 ↓
Embedding (Sentence-Transformers)
 ↓
PostgreSQL + pgvector
 ↓
Recherche sémantique (Cosine Similarity)
```

---

## 🧰 Stack technique

| Composant         | Technologie                      |
| ----------------- | -------------------------------- |
| Backend           | Django 4 + Django REST Framework |
| Base de données   | PostgreSQL                       |
| Base vectorielle  | pgvector                         |
| Modèle NLP        | Sentence-Transformers (MiniLM)   |
| Extraction PDF    | PyMuPDF                          |
| Documentation API | Swagger (drf-spectacular)        |

---

## 📦 Installation

### 1️⃣ Cloner le projet

```bash
git clone <repo-url>
cd semantic_search_api
```

### 2️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3️⃣ Configuration PostgreSQL

```sql
CREATE DATABASE semantic_db;
CREATE EXTENSION vector;
```

### 4️⃣ Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Index vectoriel (obligatoire)

```sql
CREATE INDEX chunk_embedding_idx
ON documents_documentchunk
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### 6️⃣ Lancer le serveur

```bash
python manage.py runserver
```

---

## 🔌 Endpoints disponibles

### a️⃣ Ajouter un document PDF

**POST** `/api/documents/upload-pdf/`

* Input : `title`, `file (PDF)`
* Action : extraction + chunking + embeddings

---

### b️⃣ Recherche sémantique

**GET** `/api/search/semantic/?q=...`

* Recherche par texte
* Retourne les chunks les plus proches sémantiquement

---

### c️⃣ Documents similaires

**GET** `/api/documents/{id}/similar/`

* Retourne des documents similaires à un document donné

---

### d️⃣ Historique des recherches

**GET** `/api/search/history/`

* Historique des requêtes de l’utilisateur authentifié

---

## 🔍 Exemple de réponse (Recherche)

```json
[
  {
    "document": "Cours de Data Science",
    "content": "Le machine learning est une branche...",
    "distance": 0.12
  }
]
```

---

## ⚡ Optimisations mises en place

* Index vectoriel `ivfflat` (pgvector)
* Découpage des documents en chunks
* Limitation de la taille des embeddings
* Recherche par similarité cosinus
* Architecture prête pour cache et tâches asynchrones

---

## 🎓 Justification des choix techniques

* **pgvector** : intégration native avec PostgreSQL
* **Chunking** : amélioration de la précision sémantique
* **Sentence-Transformers** : modèle léger et performant
* **API REST** : séparation claire frontend / backend

---

## 🚀 Perspectives d’amélioration

* RAG (Retrieval-Augmented Generation)
* Support Word / TXT
* OCR pour PDF scannés
* Dashboard analytics
* Cache Redis

---

## 👨‍🎓 Conclusion

Ce projet démontre la mise en œuvre complète d’une **chaîne de recherche sémantique moderne**, de l’ingestion de documents PDF jusqu’à l’exploitation d’une base vectorielle. Il constitue une base solide pour des applications industrielles telles que les moteurs de recherche intelligents, les systèmes de recommandation ou les assistants conversationnels.

---

**Projet académique – Master Data Science**
