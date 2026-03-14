"""
SVD (Singular Value Decomposition) pour recommandations

Décompose la matrice user×product en 3 matrices :
    R ≈ U × Σ × V^T

Où :
- U : matrice user × k (préférences latentes des users)
- Σ : matrice diagonale k × k (importance de chaque facteur)
- V : matrice product × k (caractéristiques latentes des produits)

Les "facteurs latents" capturent des patterns cachés :
- Facteur 1 : "aime les produits tech"
- Facteur 2 : "préfère les grandes marques"
- etc.

Pour prédire le rating d'un user U pour un produit P :
    predicted_rating = U_row · Σ · V_row^T
"""

import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds


def build_svd_model(matrix, k=50):
    """
    Construit le modèle SVD à partir de la matrice user×product.

    Args:
        matrix: DataFrame user×product avec les ratings
        k: nombre de facteurs latents (default 50)

    Returns:
        dict avec les composantes SVD et les mappings
    """
    # Centrer par la moyenne de chaque user (évite le biais vers 0)
    user_means = matrix.mean(axis=1)
    matrix_centered = matrix.sub(user_means, axis=0).fillna(0)

    # Limiter k au minimum des dimensions - 1
    k = min(k, min(matrix_centered.shape) - 1)

    # SVD sparse
    U, sigma, Vt = svds(matrix_centered.values, k=k)

    # Reconstruire les prédictions : U × Σ × V^T + moyenne user
    sigma_diag = np.diag(sigma)
    predictions_centered = U @ sigma_diag @ Vt

    # Ajouter la moyenne du user pour revenir à l'échelle originale
    predictions = predictions_centered + user_means.values.reshape(-1, 1)

    # Convertir en DataFrame
    predictions_df = pd.DataFrame(
        predictions,
        index=matrix.index,
        columns=matrix.columns
    )

    return {
        "predictions": predictions_df,
        "U": U,
        "sigma": sigma,
        "Vt": Vt,
        "k": k,
        "user_means": user_means
    }


def recommend_svd(svd_model, matrix, target_user, n=10, min_reviews=4, min_score=4.0):
    """
    Recommande les N meilleurs produits pour un user via SVD.

    Args:
        svd_model: dict retourné par build_svd_model
        matrix: DataFrame original (pour savoir ce que le user a déjà noté)
        target_user: UserId
        n: nombre de recommandations
        min_reviews: nombre minimum de reviews pour qu'un produit soit recommandé
        min_score: score minimum pour qu'un produit soit recommandé (échelle 1-5)

    Returns:
        tuple: (pd.Series avec scores, error_message)
    """
    predictions_df = svd_model["predictions"]

    # Prédictions pour ce user
    user_predictions = predictions_df.loc[target_user]

    # Produits déjà notés par le user (à exclure)
    user_ratings = matrix.loc[target_user]
    already_rated = user_ratings.dropna().index

    # Filtrer les produits avec assez de reviews
    review_counts = matrix.notna().sum(axis=0)
    valid_products = review_counts[review_counts >= min_reviews].index

    # Exclure les produits déjà achetés ET garder seulement ceux avec assez de reviews
    candidates = user_predictions.drop(already_rated, errors="ignore")
    candidates = candidates[candidates.index.isin(valid_products)]

    if len(candidates) == 0:
        return None, "Aucun produit candidat"

    # Filtrer par score minimum et trier
    result = candidates.sort_values(ascending=False)
    result = result[result >= min_score].head(n)

    if len(result) == 0:
        return None, f"Aucun produit avec score >= {min_score}"

    # Vérifier que les scores sont différenciés (pas tous identiques)
    if len(result) > 1 and result.std() < 0.01:
        return None, "Pas assez de données pour différencier les produits"

    return result, None
