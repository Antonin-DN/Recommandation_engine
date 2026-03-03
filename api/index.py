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

from services.data_loader import load_and_clean, get_products_df
from services.sentiment import analyze_sentiment, convert_polarity_to_rating, compute_adjusted_rating
from services.time_weighting import apply_time_weight
from services.product_service import get_products_details
from api.random_user import get_random_user, get_user_by_id
from services.search_service import search_products, get_similar_products

# Models
from models.user_based import build_matrix, recommend as user_based_recommend
from models.popular import get_popular_products

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache - chargé une seule fois au premier appel
_cache = {
    "df": None,           # DataFrame brut
    "df_enriched": None,  # DataFrame avec sentiment
    "products_df": None,  # DataFrame produits agrégés
    "matrix": None,       # Matrice user × product
}

def get_df():
    """Charge et cache le DataFrame brut"""
    if _cache["df"] is None:
        _cache["df"], _ = load_and_clean("data/Group6.xlsx")
    return _cache["df"]

def get_enriched_df():
    """Charge et cache le DataFrame enrichi avec sentiment + time weighting"""
    if _cache["df_enriched"] is None:
        df = get_df().copy()
        df = analyze_sentiment(df)
        df = convert_polarity_to_rating(df)
        df = compute_adjusted_rating(df)
        df = apply_time_weight(df)
        _cache["df_enriched"] = df
        print("DataFrame enrichi (sentiment + time) chargé")
    return _cache["df_enriched"]

def get_matrix():
    """Charge et cache la matrice user × product"""
    if _cache["matrix"] is None:
        df_enriched = get_enriched_df()
        _cache["matrix"] = build_matrix(df_enriched)
        print(f"Matrice chargée: {_cache['matrix'].shape[0]} users × {_cache['matrix'].shape[1]} products")
    return _cache["matrix"]

def get_cached_products_df():
    """Charge et cache le DataFrame produits"""
    if _cache["products_df"] is None:
        _cache["products_df"] = get_products_df(get_df())
        print(f"Products DF chargé: {len(_cache['products_df'])} produits")
    return _cache["products_df"]


# =============================================================================
# ROUTES API
# =============================================================================

@app.get("/api/user/random")
def random_user():
    """Retourne un user aléatoire avec son historique d'achats"""
    df = get_df()
    result = get_random_user(df)

    # Logs
    print(f"\n=== Random User ===")
    print(f"User ID: {result['user_id']}")
    print(f"Name: {result['name']}")
    print(f"Nb products: {result['nb_products']}")
    print(f"History ({len(result['history'])} items):")
    for i, h in enumerate(result['history'][:5]):
        print(f"  {i+1}. {h['ProductId']} - {h['product_name'][:30]}")
    if len(result['history']) > 5:
        print(f"  ... et {len(result['history']) - 5} autres")
    print("==================\n")

    return result


@app.get("/api/user/{user_id}")
def get_user(user_id: str):
    """Retourne un user spécifique par son ID"""
    df = get_df()
    result = get_user_by_id(df, user_id)

    if result is None:
        return {"error": f"User {user_id} non trouve"}

    # Logs
    print(f"\n=== User by ID ===")
    print(f"User ID: {result['user_id']}")
    print(f"Name: {result['name']}")
    print(f"Nb products: {result['nb_products']}")
    print("==================\n")

    return result


@app.get("/api/health")
def health():
    """Health check"""
    print("Health check OK")
    return {"status": "ok"}

# GET /api/recommendations?model=user-based&user_id=A2SUAM1J3GNN3B&n=10
@app.get("/api/recommendations")
def recommendations(model: str = "popular", user_id: str = None, n: int = 10):
    """
    Retourne les recommandations selon le modèle choisi

    Args:
        model: "popular" | "user-based" | "item-based" | "svd"
        user_id: ID du user (requis sauf pour popular)
        n: nombre de recommandations

    Returns:
        Liste de produits avec leurs infos complètes
    """
    products_df = get_cached_products_df()

    if model == "popular":
        # Top N produits basé sur weighted_rating (sentiment + temps)
        df_enriched = get_enriched_df()
        result = get_popular_products(df_enriched, n=n)

    elif model == "user-based":
        if not user_id:
            return {"error": "user_id requis pour user-based"}

        matrix = get_matrix()

        # Vérifie que le user existe dans la matrice
        if user_id not in matrix.index:
            return {"error": f"User {user_id} non trouvé dans le dataset"}

        predictions, error = user_based_recommend(matrix, user_id, k=10, n=n)

        if error:
            return {"error": error}

        result = {
            "product_ids": predictions.index.tolist(),
            "scores": predictions.values.tolist()
        }

        print(f"User-based recommendations for {user_id}: {len(result['product_ids'])} products")

    elif model == "item-based":
        return {"error": "Item-based pas encore implémenté", "products": []}

    elif model == "svd":
        return {"error": "SVD pas encore implémenté", "products": []}

    else:
        return {"error": f"Modèle inconnu: {model}"}

    # Enrichir avec les infos produits
    products = get_products_details(result, products_df)

    # Logs
    print(f"\n=== Recommendations ({model}) ===")
    print(f"User: {user_id or 'None (popular)'}")
    print(f"Count: {len(products)}")
    print("-" * 60)
    for i, p in enumerate(products):
        print(f"{i+1}. {p['name'][:40]}")
        print(f"   ID: {p['id']} | Rating: {p['rating']} | Reviews: {p['reviewCount']}")
        print(f"   Score: {p['score']} | Price: {p['price']}")
    print("=" * 60 + "\n")

    return {
        "model": model,
        "user_id": user_id,
        "count": len(products),
        "products": products
    }


@app.get("/api/search")
def search(q: str, n: int = 5):
    """
    Recherche sémantique (RAG) dans les produits

    Args:
        q: Texte de recherche
        n: Nombre de résultats (default 5)

    Returns:
        Liste de produits avec score de similarité
    """
    results = search_products(q, top_n=n)

    print(f"\n=== Search: '{q}' ===")
    print(f"Resultats: {len(results)}")
    for r in results:
        print(f"  [{r['similarity']}] {r['name'][:40]}...")
    print("=" * 40 + "\n")

    return {
        "query": q,
        "count": len(results),
        "results": results
    }


@app.get("/api/similar/{product_id}")
def similar(product_id: str, n: int = 5):
    """
    Trouve les produits similaires (basé sur embeddings)

    Args:
        product_id: ID du produit source
        n: Nombre de résultats (default 5)

    Returns:
        Liste de produits similaires avec score
    """
    results = get_similar_products(product_id, top_n=n)

    # Si erreur
    if isinstance(results, dict) and "error" in results:
        return results

    print(f"\n=== Similar to: {product_id} ===")
    print(f"Resultats: {len(results)}")
    for r in results:
        print(f"  [{r['similarity']}] {r['name'][:40]}...")
    print("=" * 40 + "\n")

    return {
        "product_id": product_id,
        "count": len(results),
        "similar": results
    }
