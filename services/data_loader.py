import pandas as pd
import json
from pathlib import Path

ENRICHED_FILE = Path(__file__).parent.parent / "data" / "products_top500.json"


def load_and_clean(filepath):
    # Charge le fichier xlsx dans un DataFrame
    df = pd.read_excel(filepath)

    # Convertit Timestamp de string en datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%d/%m/%Y  %H:%M:%S")

    # Stocke les lignes avec Reviews manquantes avant correction
    missing_reviews = df[df["Reviews"].isnull()]

    # Remplace les commentaires manquants par une string vide
    df["Reviews"] = df["Reviews"].fillna("")

    # Vérification : aucune valeur manquante restante
    no_nulls = df.isnull().sum().sum() == 0
    # Vérification : Timestamp est bien en datetime
    correct_types = df["Timestamp"].dtype == "datetime64[us]"

    is_clean = no_nulls and correct_types # les 2 doivent etre true pour valider la condition

    if is_clean:
        return df, is_clean
    else:
        print("Erreur : le dataset n'est pas clean")
        print(f"  Nulls restants : {df.isnull().sum().sum()}")
        print(f"  Types corrects : {correct_types}")
        return df, is_clean


def get_products_df(df):
    """
    Crée un DataFrame agrégé par produit

    Colonnes:
    - ProductId, product_name, avg_rating, review_count
    - category, description, embedding (depuis JSON, None si absent)
    """
    products_df = df.groupby("ProductId").agg(
        product_name=("product_name", "first"),
        avg_rating=("Rating", "mean"),
        review_count=("Rating", "count")
    ).reset_index()

    products_df["avg_rating"] = products_df["avg_rating"].round(1)

    # Enrichir avec le JSON (embeddings)
    if ENRICHED_FILE.exists():
        with open(ENRICHED_FILE, "r", encoding="utf-8") as f:
            enriched = json.load(f)

        products_df["category"] = products_df["ProductId"].map(
            lambda x: enriched.get(x, {}).get("category")
        ).fillna("")
        products_df["description"] = products_df["ProductId"].map(
            lambda x: enriched.get(x, {}).get("description")
        ).fillna("")
        products_df["embedding"] = products_df["ProductId"].map(
            lambda x: enriched.get(x, {}).get("embedding")
        )
        # Remplacer NaN par None pour embedding (liste, pas string)
        products_df["embedding"] = products_df["embedding"].where(products_df["embedding"].notna(), None)

        # Tags pour Unsplash (liste de mots-clés)
        products_df["tags"] = products_df["ProductId"].map(
            lambda x: enriched.get(x, {}).get("tags")
        )
        # Image pré-enregistrée (URL directe)
        products_df["image"] = products_df["ProductId"].map(
            lambda x: enriched.get(x, {}).get("image")
        )

        print(f"Produits enrichis: {products_df['description'].astype(bool).sum()}/{len(products_df)}")
    else:
        products_df["category"] = ""
        products_df["description"] = ""
        products_df["embedding"] = None
        products_df["tags"] = None
        products_df["image"] = None

    return products_df


# --- Code de test (exécuté uniquement en direct) ---
if __name__ == "__main__":
    df, is_clean = load_and_clean("data/Group6.xlsx")
    print(df.head())
    print(f"Clean : {is_clean}")
    print(f"Min : {df['Timestamp'].min()}")
    print(f"Max : {df['Timestamp'].max()}")
    print(f"Users distincts : {df['UserId'].nunique()}")
    print(f"Produits distincts : {df['ProductId'].nunique()}")

    # Test produits agrégés
    print("\n--- Produits agrégés ---")
    products_df = get_products_df(df)
    print(products_df.head(10))
    print(f"Total produits : {len(products_df)}")

    # Stats reviews par produit
    print("\n--- Reviews par produit ---")
    print(f"Moyenne : {products_df['review_count'].mean():.1f}")
    print(f"Médiane : {products_df['review_count'].median():.1f}")
    print(f"Max     : {products_df['review_count'].max()}")
    print(f"Produits avec 5+ reviews  : {(products_df['review_count'] >= 5).sum()}")
    print(f"Produits avec 10+ reviews : {(products_df['review_count'] >= 10).sum()}")

    # Analyse des achats groupés (même user, même jour)
    print("\n--- Achats groupes (meme user, meme jour) ---")
    df["date"] = df["Timestamp"].dt.date
    orders = df.groupby(["UserId", "date"]).agg(
        products=("ProductId", list)
    ).reset_index()

    # Garder seulement les produits UNIQUES par panier
    orders["unique_products"] = orders["products"].apply(lambda x: list(set(x)))
    orders["nb_unique"] = orders["unique_products"].apply(len)

    multi_product_orders = orders[orders["nb_unique"] > 1]
    print(f"Total 'paniers' (user+jour)       : {len(orders)}")
    print(f"Paniers avec 2+ produits UNIQUES  : {len(multi_product_orders)}")
    print(f"Pourcentage                       : {len(multi_product_orders)/len(orders)*100:.1f}%")

    if len(multi_product_orders) > 0:
        print(f"\nExemple de paniers multi-produits (uniques):")
        print(multi_product_orders[["UserId", "date", "nb_unique", "unique_products"]].head(5))

        # Compter les co-achats (paires de produits)
        from itertools import combinations
        pair_counts = {}
        for products in multi_product_orders["unique_products"]:
            for pair in combinations(sorted(products), 2):
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

        print(f"\nPaires de produits co-achetés : {len(pair_counts)}")
        top_pairs = sorted(pair_counts.items(), key=lambda x: -x[1])[:10]
        print("Top 10 paires les plus frequentes:")
        for pair, count in top_pairs:
            print(f"  {count}x : {pair[0][:10]}... + {pair[1][:10]}...")
