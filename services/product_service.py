"""
Product Service
Enrichit les IDs produits avec leurs infos complètes pour le frontend
"""

import os
import random
import requests
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env
load_dotenv()

# Clé Unsplash depuis les variables d'environnement
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


def get_products_details(recommendations, products_df):
    """
    Transforme les IDs produits en objets complets pour le frontend

    Args:
        recommendations: {
            "product_ids": ["B07XXX", "B08YYY", ...],
            "scores": [4.2, 3.9, ...]
        }
        products_df: DataFrame avec ProductId, product_name, avg_rating, review_count

    Returns:
        Liste de produits formatés pour le frontend:
        [
            {
                "id": "B07XXX",
                "name": "Casque Audio Pro",
                "rating": 4.3,
                "reviewCount": 1247,
                "price": 89.99,
                "image": "https://...",
                "score": 4.2
            },
            ...
        ]
    """
    product_ids = recommendations.get("product_ids", [])
    scores = recommendations.get("scores", [])

    products = []

    for i, product_id in enumerate(product_ids):
        # Récupère les infos du produit dans products_df
        row = products_df[products_df["ProductId"] == product_id]

        if row.empty:
            continue

        row = row.iloc[0]

        product = {
            "id": product_id,
            "name": row["product_name"],
            "rating": float(row["avg_rating"]),
            "reviewCount": int(row["review_count"]),
            "price": _generate_mock_price(),
            "image": _get_product_image(product_id, row),
            "score": float(scores[i]) if i < len(scores) else None,
            "category": row.get("category") or None,
            "description": row.get("description") or None
        }

        products.append(product)

    return products


def _generate_mock_price():
    """Génère un prix aléatoire réaliste"""
    # TODO: améliorer avec des catégories de prix
    return round(random.uniform(9.99, 299.99), 2)


def _fetch_unsplash_image(tags: list, product_id: str = None) -> str | None:
    """
    Cherche une image sur Unsplash avec les tags

    Args:
        tags: Liste de mots-clés (ex: ["headphones", "audio", "wireless"])
        product_id: ID du produit (pour le log)

    Returns:
        URL de l'image ou None si échec
    """
    if not UNSPLASH_ACCESS_KEY:
        print(f"[Unsplash] Pas de clé API configurée")
        return None

    query = " ".join(tags)
    print(f"[Unsplash] Requête: '{query}' (produit: {product_id})")

    try:
        res = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": query, "per_page": 1},
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=5
        )
        res.raise_for_status()
        data = res.json()

        if data.get("results"):
            url = data["results"][0]["urls"]["small"]
            print(f"[Unsplash] OK: {url[:60]}...")
            return url

        print(f"[Unsplash] Aucun resultat pour '{query}'")
        return None
    except Exception as e:
        print(f"[Unsplash] Erreur: {e}")
        return None


def _get_product_image(product_id: str, row) -> str:
    """
    Retourne l'URL de l'image avec priorité :
    1. Image pré-enregistrée dans le JSON
    2. Unsplash avec les tags
    3. Fallback picsum (random)
    """
    # 1. Image pré-enregistrée
    image = row.get("image")
    if image and str(image) != "nan":
        return image

    # 2. Unsplash avec tags
    tags = row.get("tags")
    if tags and isinstance(tags, list):
        unsplash_image = _fetch_unsplash_image(tags, product_id)
        if unsplash_image:
            return unsplash_image

    # 3. Fallback picsum
    return f"https://picsum.photos/seed/{product_id[:8]}/300/300"
