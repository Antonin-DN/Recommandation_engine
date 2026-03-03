"""
Script one-shot pour générer descriptions, catégories et embeddings
pour les TOP 500 produits (les plus reviewés).

Output: data/products_top500.json (~10 MB)
- Utilisé pour la recherche sémantique (RAG)
- Utilisé pour les produits similaires
"""

import argparse
import json
import time
from pathlib import Path

from data_loader import load_and_clean, get_products_df
from ollama_service import (
    generate_description,
    categorize_product,
    get_embedding,
    check_ollama_status,
    list_models
)


OUTPUT_FILE = Path(__file__).parent.parent / "data" / "products_top500.json"
DEFAULT_LIMIT = 500


def get_reviews_for_product(df, product_id: str, max_reviews: int = 3) -> list[str]:
    """Récupère les reviews d'un produit"""
    reviews = df[df["ProductId"] == product_id]["Reviews"].tolist()
    # Filtrer les reviews vides et prendre les max_reviews premières
    reviews = [r for r in reviews if r and len(r) > 10]
    return reviews[:max_reviews]


def process_products(df, products_df, limit: int = None, model: str = "mistral", existing: dict = None):
    """
    Génère description, catégorie et embedding pour chaque produit

    Args:
        df: DataFrame complet avec les reviews
        products_df: DataFrame agrégé par produit
        limit: Nombre max de produits à traiter (None = tous)
        model: Modèle Ollama pour génération de texte
        existing: Résultats existants à conserver (pour reprise)
    """
    products = products_df.to_dict("records")

    if limit:
        products = products[:limit]

    total = len(products)
    results = existing.copy() if existing else {}
    skipped = 0
    start_time = time.time()

    print(f"\nTraitement de {total} produits avec le modele '{model}'...\n")

    for i, product in enumerate(products):
        product_id = product["ProductId"]
        product_name = product["product_name"]

        # Skip si déjà traité
        if product_id in results:
            skipped += 1
            continue

        # Progression (compte seulement les non-skippés)
        processed = i - skipped
        elapsed = time.time() - start_time
        remaining_count = total - i
        if processed > 0:
            avg_time = elapsed / processed
            remaining = avg_time * remaining_count
            print(f"[{i+1}/{total}] {product_id[:15]}... (reste ~{remaining:.0f}s)")
        else:
            print(f"[{i+1}/{total}] {product_id[:15]}...")

        # Récupérer les reviews
        reviews = get_reviews_for_product(df, product_id)

        # Générer description
        description = generate_description(product_name, reviews, model=model)
        if not description:
            print(f"  ERREUR description, skip")
            continue

        # Catégoriser
        category = categorize_product(product_name, description, model=model)

        # Embedding
        embedding = get_embedding(description)

        results[product_id] = {
            "name": product_name,
            "description": description,
            "category": category,
            "embedding": embedding,
            "review_count": product["review_count"],
            "avg_rating": product["avg_rating"]
        }

        # Afficher exemple pour les premiers
        if i < 3:
            print(f"  Nom: {product_name[:50]}...")
            print(f"  Desc: {description[:80]}...")
            print(f"  Cat: {category}")
            print(f"  Emb: {len(embedding) if embedding else 0} dimensions")
            print()

    if skipped > 0:
        print(f"\n{skipped} produits deja traites (skip)")

    return results


def load_existing_results(output_path: Path) -> dict:
    """Charge les résultats existants pour reprendre"""
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_results(results: dict, output_path: Path):
    """Sauvegarde les résultats en JSON"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResultats sauvegardes dans: {output_path}")
    print(f"Taille: {output_path.stat().st_size / 1024 / 1024:.1f} MB")


def main():
    parser = argparse.ArgumentParser(description="Génère embeddings pour les produits")
    parser.add_argument("--limit", type=int, help="Nombre max de produits à traiter")
    parser.add_argument("--model", default="mistral", help="Modèle Ollama (default: mistral)")
    args = parser.parse_args()

    print("=== Embeddings Generator ===\n")

    # Check Ollama
    if not check_ollama_status():
        print("ERREUR: Ollama n'est pas accessible")
        print("Lance 'ollama serve' dans un terminal")
        return

    models = list_models()
    print(f"Modeles disponibles: {models}")

    if args.model not in [m.split(":")[0] for m in models]:
        print(f"\nATTENTION: Le modele '{args.model}' n'est peut-etre pas installe")
        print(f"Fais: ollama pull {args.model}")

    # Charger les données
    print("\nChargement des donnees...")
    df, _ = load_and_clean("data/Group6.xlsx")
    products_df = get_products_df(df)
    print(f"Produits total: {len(products_df)}")

    # Trier par nombre de reviews (les plus reviewés en premier)
    products_df = products_df.sort_values("review_count", ascending=False)

    # Limiter aux top N (default 500)
    limit = args.limit if args.limit else DEFAULT_LIMIT
    print(f"Selection des top {limit} produits (les plus reviewes)")
    print(f"Min reviews dans selection: {products_df.head(limit)['review_count'].min()}")

    # Charger résultats existants (pour reprendre)
    existing_results = load_existing_results(OUTPUT_FILE)
    if existing_results:
        print(f"\nReprise: {len(existing_results)} produits deja traites")

    # Traiter les produits (en passant les existants pour les skip)
    results = process_products(df, products_df, limit=limit, model=args.model, existing=existing_results)

    # Stats
    print(f"\n=== Stats ===")
    print(f"Produits traites: {len(results)}")
    categories = {}
    for p in results.values():
        cat = p.get("category", "Autre")
        categories[cat] = categories.get(cat, 0) + 1
    print(f"Categories: {categories}")

    # Sauvegarder
    if results:
        save_results(results, OUTPUT_FILE)


if __name__ == "__main__":
    main()
