"""
Popular Model
Retourne les produits les plus populaires avec un score qui équilibre
la qualité (rating) et la popularité (nombre de reviews)
"""

import pandas as pd
import numpy as np


def get_popular_products(df_enriched, n=10, min_reviews=5):
    """
    Retourne les N produits les plus populaires

    Formule du score: avg_rating * log(review_count + 1)
    - Favorise les produits avec beaucoup de reviews ET de bonnes notes
    - Un produit 5 étoiles avec 5 reviews < produit 4.5 étoiles avec 50 reviews

    Args:
        df_enriched: DataFrame avec weighted_rating
        n: nombre de produits à retourner
        min_reviews: minimum de reviews pour être considéré

    Returns:
        {
            "product_ids": ["B07XXX", ...],
            "scores": [12.5, 11.3, ...]
        }
    """
    # Agrège par produit
    popular = df_enriched.groupby("ProductId").agg(
        avg_rating=("weighted_rating", "mean"),
        review_count=("weighted_rating", "count")
    ).reset_index()

    # Filtre les produits avec peu de reviews
    popular = popular[popular["review_count"] >= min_reviews]

    # Score = rating * log(review_count + 1)
    # Équilibre qualité et popularité
    popular["score"] = popular["avg_rating"] * np.log1p(popular["review_count"])

    # Trie par score décroissant
    popular = popular.nlargest(n, "score")

    return {
        "product_ids": popular["ProductId"].tolist(),
        "scores": popular["score"].round(2).tolist()
    }


# --- Test ---
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from services.data_loader import load_and_clean, get_products_df
    from services.sentiment import analyze_sentiment, convert_polarity_to_rating, compute_adjusted_rating
    from services.time_weighting import apply_time_weight

    df, _ = load_and_clean("data/Group6.xlsx")
    df = analyze_sentiment(df)
    df = convert_polarity_to_rating(df)
    df = compute_adjusted_rating(df)
    df = apply_time_weight(df)

    products_df = get_products_df(df)
    result = get_popular_products(df, n=10)

    print("Top 10 produits populaires (score = rating * log(reviews)):")
    print("-" * 70)
    for i, (pid, score) in enumerate(zip(result["product_ids"], result["scores"])):
        prod = products_df[products_df["ProductId"] == pid].iloc[0]
        print(f"{i+1:2}. {prod['product_name'][:40]}")
        print(f"    Rating: {prod['avg_rating']} | Reviews: {prod['review_count']} | Score: {score}")
    print("-" * 70)
