"""
Product Service
Enrichit les IDs produits avec leurs infos complètes pour le frontend
"""

import random


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
            "image": _generate_mock_image(product_id),
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


def _generate_mock_image(product_id):
    """
    Génère une URL d'image placeholder

    TODO: Intégrer Unsplash API avec description Ollama
    """
    # Placeholder pour l'instant
    return f"https://picsum.photos/seed/{product_id[:8]}/300/300"
