# =============================================================================
# MOTEUR DE RECOMMANDATION
# =============================================================================

# STEP 1: Import & Load Data
# - Charger le fichier xlsx (Group1.xlsx)
# - Colonnes attendues: user_id, product_id, rating, comment

# STEP 2: Sentiment Analysis
# - Analyser le sentiment de chaque commentaire (TextBlob)
# - Score sentiment: -1 (négatif) à +1 (positif)

# STEP 3: Score Pondéré
# - Combiner rating + sentiment pour créer un score pondéré
# - Formule: score = rating * (1 + sentiment * weight)

# STEP 4: Matrice User-Product
# - Créer une matrice users (lignes) x products (colonnes)
# - Valeurs = scores pondérés

# STEP 5: Similarité Users
# - Calculer corrélation entre users (Pearson ou Cosine)
# - Trouver les K users les plus similaires à l'user cible

# STEP 6: Recommandations
# - Identifier produits achetés par users similaires
# - Exclure produits déjà achetés par l'user cible
# - Calculer moyenne pondérée des scores
# - Retourner top N produits avec meilleure moyenne

# =============================================================================
# 3 MODÈLES DE RECOMMANDATION
# =============================================================================
#
# 1. USER-BASED COLLABORATIVE FILTERING
#    - Trouve des users avec des goûts similaires (corrélation Pearson)
#    - Recommande ce que les users similaires ont aimé
#    - Simple mais sensible au cold start
#
# 2. ITEM-BASED COLLABORATIVE FILTERING
#    - Trouve des produits similaires (achetés par les mêmes users)
#    - "Les gens qui ont aimé X ont aussi aimé Y"
#    - Plus stable, les relations produits changent moins
#
# 3. MATRIX FACTORIZATION (SVD)
#    - Décompose la matrice user-product en facteurs latents
#    - Capture des patterns cachés (ex: "aime le style minimaliste")
#    - Plus précis, gère mieux les données sparse
#    - Utilisé par Netflix
#
# =============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.data_loader import load_and_clean
from api.random_user import get_random_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache du DataFrame - chargé une seule fois au premier appel
_df_cache = None

def get_df():
    """Charge et cache le DataFrame pour éviter de recharger à chaque requête"""
    global _df_cache
    if _df_cache is None:
        _df_cache, _ = load_and_clean("data/Group6.xlsx")
    return _df_cache


# =============================================================================
# ROUTES API
# =============================================================================

@app.get("/api/user/random")
def random_user():
    """Retourne un user aléatoire avec son historique d'achats"""
    df = get_df()
    return get_random_user(df)


@app.get("/api/health")
def health():
    """Health check"""
    return {"status": "ok"}
