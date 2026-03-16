"""
Script pour ajouter des tags (mots-clés) aux produits existants.
Les tags servent pour la recherche d'images Unsplash.

Charge le JSON existant, génère les tags manquants, sauvegarde.
"""

import argparse
import json
import time
from pathlib import Path

from ollama_service import generate_tags, check_ollama_status, list_models


INPUT_FILE = Path(__file__).parent.parent / "data" / "products_top500.json"


def load_products(file_path: Path) -> dict:
    """Charge le fichier JSON existant"""
    if not file_path.exists():
        print(f"ERREUR: Fichier non trouvé: {file_path}")
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_products(products: dict, file_path: Path):
    """Sauvegarde le fichier JSON"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"\nSauvegardé: {file_path}")
    print(f"Taille: {file_path.stat().st_size / 1024 / 1024:.1f} MB")


def process_tags(products: dict, model: str = "mistral", limit: int = None):
    """
    Génère les tags pour les produits qui n'en ont pas encore.

    Args:
        products: Dict des produits (modifié in-place)
        model: Modèle Ollama
        limit: Nombre max de produits à traiter (None = tous)
    """
    # Compter les produits sans tags
    products_without_tags = [
        (pid, p) for pid, p in products.items()
        if not p.get("tags")
    ]

    if limit:
        products_without_tags = products_without_tags[:limit]

    total = len(products_without_tags)
    if total == 0:
        print("Tous les produits ont déjà des tags!")
        return 0

    print(f"\n{total} produits sans tags à traiter...\n")

    processed = 0
    errors = 0
    start_time = time.time()

    for i, (product_id, product) in enumerate(products_without_tags):
        product_name = product.get("name", "Unknown")
        description = product.get("description", "")

        # Progression
        elapsed = time.time() - start_time
        if processed > 0:
            avg_time = elapsed / processed
            remaining = avg_time * (total - i)
            print(f"[{i+1}/{total}] {product_name[:40]}... (reste ~{remaining:.0f}s)")
        else:
            print(f"[{i+1}/{total}] {product_name[:40]}...")

        # Générer tags
        tags = generate_tags(product_name, description, model=model)

        if tags:
            products[product_id]["tags"] = tags
            processed += 1

            # Afficher les premiers pour vérification
            if i < 5:
                print(f"  -> Tags: {tags}")
        else:
            print(f"  -> ERREUR, pas de tags générés")
            errors += 1

    print(f"\n=== Résumé ===")
    print(f"Traités: {processed}")
    print(f"Erreurs: {errors}")

    return processed


def main():
    parser = argparse.ArgumentParser(description="Génère des tags pour les produits")
    parser.add_argument("--limit", type=int, help="Nombre max de produits à traiter")
    parser.add_argument("--model", default="mistral", help="Modèle Ollama (default: mistral)")
    parser.add_argument("--input", type=str, help="Fichier JSON source (default: products_top500.json)")
    args = parser.parse_args()

    print("=== Tags Generator ===\n")

    # Check Ollama
    if not check_ollama_status():
        print("ERREUR: Ollama n'est pas accessible")
        print("Lance 'ollama serve' dans un terminal")
        return

    models = list_models()
    print(f"Modèles disponibles: {models}")

    # Fichier source
    input_file = Path(args.input) if args.input else INPUT_FILE

    # Charger les produits
    print(f"\nChargement: {input_file}")
    products = load_products(input_file)

    if not products:
        return

    print(f"Produits chargés: {len(products)}")

    # Stats avant
    with_tags = sum(1 for p in products.values() if p.get("tags"))
    print(f"Avec tags: {with_tags}")
    print(f"Sans tags: {len(products) - with_tags}")

    # Générer les tags manquants
    processed = process_tags(products, model=args.model, limit=args.limit)

    # Sauvegarder si modifications
    if processed > 0:
        save_products(products, input_file)


if __name__ == "__main__":
    main()
