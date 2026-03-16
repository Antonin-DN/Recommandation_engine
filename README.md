User-Based Collaborative Filtering (le plus simple)
Item-Based Collaborative Filtering (symétrique du user-based)
Matrix Factorization (SVD) (plus puissant)
SVD avec pondération temporelle (le plus sophistiqué)


  Chose à rajouter dans data loader : 
  - Moyenne global de tout les avis et nombres d'avis au data frame, prix random 

  API :
  Une route pour générer un profil user random dans le dataset, on selectionne un puis on récupère son historique de commande
  Une route pour générer la recommandation basée sur le modèle
  Les photos a voir en fonction du nombre de produit (count distinct)


  ---------------------------------------------- GEPHI
  En regroupant par user_id + date/heure d'achat, vous capturez les produits achetés dans la même session, ce qui est une signal beaucoup plus fort. "Ces deux produits ont été achetés ensemble consciemment, le même jour, par la même personne" est plus puissant que "ces deux produits plaisent aux mêmes personnes en général".
  Option 1 — La visualisation réseau comme dans Gephi
Vous construisez exactement le même type de graphe qu'aujourd'hui mais avec vos données. Chaque co-achat dans un panier = une arête. Vous identifiez vos hubs, vos produits isolés, vos ponts entre catégories. En Python avec NetworkX c'est une dizaine de lignes de code.

Option 2 — L'algorithme Apriori ou FP-Growth
C'est l'approche classique pour l'analyse de paniers. L'idée est de trouver des règles d'association du type "les clients qui achètent A et B achètent aussi C dans 70% des cas". C'est plus directement exploitable pour la recommandation que la visualisation réseau.

Option 3 — Combiner les deux approches
Vous utilisez la visualisation réseau pour comprendre et nettoyer votre catalogue (identifier les produits trop isolés, les hubs), puis vous alimentez votre modèle item-based existant avec les corrélations issues des paniers en plus des similarités utilisateur. Votre recommandation devient plus précise.


---

## Projet

Application de **comparaison de systèmes de recommandation** appliqués à un dataset Amazon. L'objectif est d'évaluer les performances de différentes approches de filtrage collaboratif sur des données réelles d'avis produits.

### Objectifs

- Comparer 3 algorithmes de recommandation (User-Based CF, Item-Based CF, SVD)
- Visualiser les recommandations via une interface interactive
- Mesurer et afficher les métriques de performance (précision, rappel, etc.)

### Enrichissement des données

Pour rendre l'application plus réaliste et visuelle :
- **Prix des articles** : générés aléatoirement
- **Noms des utilisateurs** : générés avec Faker
- **Descriptions produits** : générées via Ollama (LLM local)
- **Catégories** : extraites pour permettre une recherche RAG basique

---

## Dataset

| Statistique | Valeur |
|-------------|--------|
| Période | 2003 - 2023 |
| Utilisateurs distincts | 7 023 |
| Produits distincts | 8 623 |
| Sparsité : 99.98%
Min : 2003-01-11 07:45:02
Max : 2023-05-15 04:47:27
Users distincts : 7023
Produits distincts : 8623

=== TOP 10 USERS PAR NOMBRE DE COMMANDES ===
     1. AG73BVBKUOH22USSFJA5ZWL7AKXA : 95 commandes
     2. AEZP6Z2C5AVQDZAJECQYZWQRNG3Q : 74 commandes
     3. AEMP3A7IKW37CMWFXNKXWW6HGJHA_1 : 66 commandes
     4. AFXF3EGQTQDXMRLDWFU7UBFQZB7Q : 64 commandes
     5. AGZUJTI7A3JFKB4FP5JOH6NVAJIQ_1 : 56 commandes
     6. AEJU3Z6HDAERETMYI2CXBQVPPDFA : 39 commandes
     7. AEOK4TQIKGO23SJKZ6PW4FETNNDA_1 : 38 commandes
     8. AGOLMT3QETKYNESRYKBA6D7XXS7A : 36 commandes
     9. AH3BXW7KLIS2VAE56UXJS2NS7I5A : 36 commandes
     10. AEAXAJACFMXIAAH4WOHRMXPSZWFA : 34 commandes

┌─────────┬───────┬──────────┬──────────┐
  │ Dataset │ Users │ Produits │ Sparsité │
  ├─────────┼───────┼──────────┼──────────┤
  │ Complet │ 7023  │ 8623     │ 99.97%   │
  ├─────────┼───────┼──────────┼──────────┤
  │ ≥3 cmd  │ 2798  │ 5507     │ 99.91%   │
  ├─────────┼───────┼──────────┼──────────┤
  │ ≥5 cmd  │ 893   │ 2855     │ 99.71%   │

### Limitations

Le dataset étant anonymisé, nous ne disposons pas :
- Des informations démographiques (âge, sexe, pays) qui auraient pu améliorer les recommandations
- Des caractéristiques détaillées des produits (dimensions, marque, etc.)

Ces limitations impactent notamment la gestion du **cold start problem**.

---

## Challenges : Sparsité extrême

### Le problème

| Métrique | Valeur |
|----------|--------|
| Sparsité de la matrice | **99.98%** |
| Reviews/utilisateur (moyenne) | 2.1 |
| Reviews/produit (moyenne) | 2.3 |

Avec si peu d'interactions, les algorithmes de filtrage collaboratif (User-Based, Item-Based) peinent à trouver des similarités significatives.

### Tentative : Analyse de paniers (Market Basket)

L'idée était d'exploiter les **co-achats** (produits achetés ensemble le même jour par un utilisateur) pour construire un graphe de relations produits et identifier des "hubs".

| Métrique | Valeur |
|----------|--------|
| Total paniers (user+jour) | 13 963 |
| Paniers avec 2+ produits uniques | 617 (4.4%) |
| Paire la plus fréquente | **3 occurrences** |

**Verdict** : Non exploitable. La paire de produits la plus achetée ensemble n'apparaît que 3 fois. Pour du network analysis significatif, il faudrait des paires à 50+ occurrences. La sparsité impacte aussi cette approche.

### Solutions avec des features supplémentaires

#### Features Utilisateurs (non disponibles)
Avec des données démographiques (âge, sexe, localisation, historique de navigation), on pourrait :
- **Clustering d'utilisateurs** : regrouper les users par profil similaire
- **Prédiction par cluster** : un user avec 2 achats hérite des préférences de son cluster
- Réduction du cold start pour les nouveaux utilisateurs

#### Features Produits (partiellement disponibles)
Avec des caractéristiques produits (catégorie, marque, description, prix), on pourrait :
- **Content-Based Filtering** : recommander des produits similaires par leurs attributs
- **Embeddings de descriptions** : vectoriser les descriptions avec un LLM
- **Similarité sémantique** : trouver des produits proches même sans historique commun

### Notre approche : Enrichissement via Ollama

Pour pallier le manque de features, nous utilisons **Ollama** (LLM local) pour :
1. **Générer des descriptions** détaillées à partir des noms de produits
2. **Créer des embeddings** vectoriels de ces descriptions
3. **Clustering automatique** des produits par similarité sémantique
4. **Hybrid Recommender** : CF quand possible, content-based en fallback

---

## Stack Technique

### Backend (Python)
- **FastAPI** : API REST
- **Pandas / NumPy** : manipulation des données
- **Scikit-learn** : calcul de similarité (cosine)
- **TextBlob** : analyse de sentiment
- **Faker** : génération de données mock

### Frontend (React)
- **Vite** : bundler
- **Zustand** : state management
- **Tailwind CSS** : styling
- **Lucide React** : icônes

### Déploiement
- **Vercel** : hébergement frontend + serverless functions Python

---

## Structure du projet

```
recommandation_engine_app/
├── api/                    # Backend FastAPI
│   ├── index.py            # Point d'entrée API
│   └── random_user.py      # Génération user aléatoire
├── services/               # Logique métier Python
│   └── data_loader.py      # Chargement et nettoyage données
├── models/                 # Modèles de recommandation
├── src/                    # Frontend React
│   ├── components/         # Composants UI
│   ├── pages/              # Pages
│   └── stores/             # Zustand stores
└── data/                   # Dataset Excel
```

---

## Installation

```bash
# Frontend
npm install

# Backend (Python)
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Lancement

```bash
npm start  # Lance frontend + backend simultanément
```

---

## API Endpoints

| Route | Description |
|-------|-------------|
| `GET /api/health` | Health check |
| `GET /api/user/random` | Génère un utilisateur aléatoire avec son historique |
| `GET /api/recommendations` | Recommandations selon le modèle (à venir) | 

