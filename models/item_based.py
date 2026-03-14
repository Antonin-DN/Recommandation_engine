"""
Item-based Collaborative Filtering

On compare 2 produits sur les notes données par les MÊMES users.

              User1   User2   User3   User4   User5
Produit A       5       4       -       5       3
Produit B       4       5       -       4       4
Produit C       -       1       5       -       2

Pour comparer A et B :
- On regarde les users qui ont noté les deux : User1, User2, User4, User5
- A : [5, 4, 5, 3]
- B : [4, 5, 4, 4]
- On calcule la similarité cosinus sur ces 4 paires
Score(Produit X) = Σ (similarité(X, produit_acheté) × note_donnée) / Σ similarités

  Exemple

  User a acheté :
  - Casque Sony → noté 5
  - Clavier Logitech → noté 2

  Pour prédire le score de la Souris Logitech :
  ┌──────────────────┬────────────────────────┬─────────────┬─────────────────┐
  │  Produit acheté  │ Similarité avec Souris │ Note donnée │  Contribution   │
  ├──────────────────┼────────────────────────┼─────────────┼─────────────────┤
  │ Casque Sony      │ 0.30                   │ 5           │ 0.30 × 5 = 1.5  │
  ├──────────────────┼────────────────────────┼─────────────┼─────────────────┤
  │ Clavier Logitech │ 0.88                   │ 2           │ 0.88 × 2 = 1.76 │
  └──────────────────┴────────────────────────┴─────────────┴─────────────────┘
  Score Souris = (1.5 + 1.76) / (0.30 + 0.88) = 3.26 / 1.18 = 2.76

  La souris est très similaire au clavier (0.88), mais le user a mal noté le clavier (2), donc le score final est tiré
  vers le bas.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def build_item_similarity(matrix):
    """
    Calcule la matrice de similarité entre tous les produits.

    Args:
        matrix: DataFrame user×product (lignes=users, colonnes=products)

    Returns:
        DataFrame product×product avec les scores de similarité cosinus

    Formule cosinus:
        cos(A,B) = (A · B) / (||A|| × ||B||)
                 = Σ(Ai × Bi) / (√Σ Ai² × √Σ Bi²)
    """

    # Step 1 : Remplacer les NaN par 0 (cosine_similarity n'accepte pas les NaN)
    matrix_filled = matrix.fillna(0)

    # Step 2 : Transposer la matrice (products en lignes pour comparer les produits)
    matrix_T = matrix_filled.T

    # Step 3 : Calculer la similarité cosinus entre toutes les paires de produits
    similarity = cosine_similarity(matrix_T)

    # Step 4 : Convertir en DataFrame avec les ProductId en index et colonnes
    item_similarity = pd.DataFrame(
        similarity,
        index=matrix.columns,
        columns=matrix.columns
    )

    return item_similarity


def recommend_item_based(item_similarity, matrix, target_user, n=10, min_reviews=4, min_score=4.0):
    """
    Recommande les N meilleurs produits pour un user basé sur la similarité items.

    Args:
        item_similarity: DataFrame product×product (précalculée)
        matrix: DataFrame user×product avec les ratings
        target_user: UserId
        n: nombre de recommandations à retourner
        min_reviews: nombre minimum de reviews pour qu'un produit soit recommandé
        min_score: score minimum pour qu'un produit soit recommandé (échelle 1-5)

    Returns:
        tuple: (pd.Series avec scores, error_message)
    """
    # Step 1 : Récupérer les ratings du user
    user_ratings = matrix.loc[target_user]

    # Produits notés par le user (non-NaN)
    rated_products = user_ratings.dropna()

    # Produits candidats (non notés)
    unrated_products = user_ratings[user_ratings.isna()].index

    # Filtrer les produits avec assez de reviews
    review_counts = matrix.notna().sum(axis=0)  # nb de ratings par produit
    valid_products = review_counts[review_counts >= min_reviews].index
    unrated_products = unrated_products.intersection(valid_products)

    # Step 2 : Calculer le score prédit pour chaque produit non noté
    predictions = {}

    for candidate in unrated_products:
        if candidate not in item_similarity.index:
            continue

        # Similarités entre ce candidat et les produits notés par le user
        similarities = item_similarity.loc[candidate, rated_products.index]

        # Garde seulement les similarités positives
        positive_sims = similarities[similarities > 0]

        if len(positive_sims) == 0:
            continue

        # Ratings correspondants
        ratings = rated_products[positive_sims.index]

        # Score = moyenne pondérée par similarité
        predicted_score = (positive_sims * ratings).sum() / positive_sims.sum()
        predictions[candidate] = predicted_score

    if len(predictions) == 0:
        return None, "Aucune prédiction possible"

    # Step 3 : Filtrer par score minimum et retourner le top N
    result = pd.Series(predictions).sort_values(ascending=False)
    result = result[result >= min_score].head(n)

    if len(result) == 0:
        return None, f"Aucun produit avec score >= {min_score}"

    # Vérifier que les scores sont différenciés
    if len(result) > 1 and result.std() < 0.01:
        return None, "Pas assez de données pour différencier les produits"

    return result, None


# --- Test ---
if __name__ == "__main__":
    pass
