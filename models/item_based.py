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


def recommend_item_based(item_similarity, df, target_user=None, n=5):
    """
    Recommande les N meilleurs produits pour un user basé sur la similarité items.

    Args:
        item_similarity: DataFrame product×product (précalculée)
        df: DataFrame original avec l'historique des users
        target_user: UserId (optionnel, si None on génère un user aléatoire)
        n: nombre de recommandations à retourner

    Returns:
        tuple: (recommendations, user_info) ou (None, error)
    """

    # Step 1 : Si target_user est None, en sélectionner un aléatoirement

    # Step 2 : Récupérer l'historique du user (produits notés + notes)

    # Step 3 : Pour chaque produit NON acheté, calculer un score prédit
    #          Score = moyenne pondérée des similarités avec les produits achetés

    # Step 4 : Trier par score décroissant et retourner le top N

    pass


# --- Test ---
if __name__ == "__main__":
    pass
