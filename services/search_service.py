"""
Service de recherche sémantique (RAG) et produits similaires
Utilise les embeddings pré-générés dans products_top500.json
"""

import json
import numpy as np
from pathlib import Path

EMBEDDINGS_FILE = Path(__file__).parent.parent / "data" / "products_top500.json"

# Cache des produits chargés
_products_cache = None


def load_products() -> dict:
    """Charge les produits avec embeddings (avec cache)"""
    global _products_cache
    if _products_cache is None:
        with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
            _products_cache = json.load(f)
    return _products_cache


def cosine_similarity(vec1: list, vec2: list) -> float:
    """Calcule la similarité cosinus entre deux vecteurs"""
    a = np.array(vec1)
    b = np.array(vec2)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_products(query: str, top_n: int = 5) -> list:
    """
    Recherche par mots-clés (fonctionne sans Ollama)

    Args:
        query: Texte de recherche
        top_n: Nombre de résultats

    Returns:
        Liste de produits avec score de pertinence
    """
    products = load_products()
    query_lower = query.lower()
    query_words = query_lower.split()

    results = []
    for product_id, product in products.items():
        name = (product.get("name") or "").lower()
        desc = (product.get("description") or "").lower()
        text = f"{name} {desc}"

        # Score = proportion de mots trouvés
        score = sum(1 for word in query_words if word in text)

        if score > 0:
            results.append({
                "product_id": product_id,
                "name": product["name"],
                "description": product["description"],
                "category": product["category"],
                "avg_rating": product.get("avg_rating", 4.0),
                "review_count": product.get("review_count", 0),
                "similarity": round(score / len(query_words), 2)
            })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_n]


def get_similar_products(product_id: str, top_n: int = 5) -> list:
    """
    Trouve les produits similaires à un produit donné

    Args:
        product_id: ID du produit source
        top_n: Nombre de résultats

    Returns:
        Liste de produits similaires avec score
    """
    products = load_products()

    # Vérifier que le produit existe et a un embedding
    if product_id not in products:
        return {"error": f"Produit {product_id} non trouvé"}

    source = products[product_id]
    if not source.get("embedding"):
        return {"error": f"Pas d'embedding pour {product_id}"}

    source_embedding = source["embedding"]

    # Calculer la similarité avec les autres produits
    results = []
    for pid, product in products.items():
        if pid == product_id:
            continue
        if product.get("embedding"):
            similarity = cosine_similarity(source_embedding, product["embedding"])
            results.append({
                "product_id": pid,
                "name": product["name"],
                "description": product["description"],
                "category": product["category"],
                "avg_rating": product.get("avg_rating", 4.0),
                "review_count": product.get("review_count", 0),
                "similarity": round(similarity, 3)
            })

    # Trier par similarité décroissante
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:top_n]


# --- Test ---
if __name__ == "__main__":
    print("=== Test Search Service ===\n")

    products = load_products()
    print(f"Produits charges: {len(products)}\n")

    # Test recherche
    print("--- Recherche: 'ecouteurs bluetooth' ---")
    results = search_products("ecouteurs bluetooth", top_n=3)
    for r in results:
        print(f"  [{r['similarity']}] {r['name'][:50]}...")

    # Test produits similaires
    print("\n--- Produits similaires au premier resultat ---")
    if results:
        first_id = results[0]["product_id"]
        similar = get_similar_products(first_id, top_n=3)
        for s in similar:
            print(f"  [{s['similarity']}] {s['name'][:50]}...")
