import pandas as pd
import numpy as np


def build_matrix(df):
    """Crée la matrice user × product avec adjusted_rating"""

    matrix = df.pivot_table(
        index="UserId",
        columns="ProductId",
        values="adjusted_rating"
    )

    return matrix


def get_similar_users(matrix, target_user, k=10, min_products=3):
    """Trouve les K users les plus similaires au target_user"""

    # Récupère les ratings du user cible (une ligne de la matrice et stock un vecteur sous forme de list)
    target_ratings = matrix.loc[target_user]

    # Vérifie que le user a assez de produits notés (cold start problème)
    nb_products = target_ratings.notna().sum() 
    if nb_products < min_products:
        return None, f"Pas assez de reviews ({nb_products} < {min_products})"

    # Calcule la corrélation de Pearson avec tous les autres users, corrélation linéaire entre -1 et 1
    # Corrélation = (Covariance de X et Y) / (Écart-type de X × Écart-type de Y)
    # ✗ L'intensité absolue des notes ✗ La sévérité ou générosité de notation ✗ L'échelle personnelle utilisée
    correlations = matrix.T.corrwith(target_ratings)

    # Enlève le user lui-même et les NaN (pas assez de produits en commun)
    correlations = correlations.drop(target_user, errors="ignore")
    correlations = correlations.dropna()

    # Vérifie qu'on a trouvé des users similaires
    if len(correlations) == 0:
        return None, "No similar users found"

    # Trie par corrélation décroissante et prend les K premiers
    similar_users = correlations.sort_values(ascending=False).head(k)

    return similar_users, None


def predict_ratings(matrix, target_user, similar_users):
    """Prédit les notes pour les produits non notés par le user cible"""

    # Produits que le user cible n'a PAS notés
    target_ratings = matrix.loc[target_user]
    unrated_products = target_ratings[target_ratings.isna()].index

    predictions = {}

    for product in unrated_products:
        # Notes des users similaires pour ce produit
        ratings = matrix.loc[similar_users.index, product]

        # Garde seulement ceux qui ont noté ce produit
        valid = ratings.dropna()

        if len(valid) == 0:
            continue

        # Corrélations correspondantes (poids)
        weights = similar_users[valid.index]

        # Moyenne pondérée par la corrélation
        predicted_rating = (valid * weights).sum() / weights.sum()
        predictions[product] = predicted_rating

    return pd.Series(predictions).sort_values(ascending=False)


def recommend(matrix, target_user, k=10, n=5):
    """Recommande les N meilleurs produits pour un user"""

    similar_users, error = get_similar_users(matrix, target_user, k=k)
    if error:
        return None, error

    predictions = predict_ratings(matrix, target_user, similar_users)

    if len(predictions) == 0:
        return None, "Aucune prédiction possible"

    return predictions.head(n), None


# --- Test ---
if __name__ == "__main__":
    import sys
    import os
    # Ajoute le dossier parent au path pour accéder à services/
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from services.data_loader import load_and_clean
    from services.sentiment import analyze_sentiment, convert_polarity_to_rating, compute_adjusted_rating

    df, is_clean = load_and_clean("data/Group6.xlsx")
    df = analyze_sentiment(df)
    df = convert_polarity_to_rating(df)
    df = compute_adjusted_rating(df)

    matrix = build_matrix(df)
    print(f"Matrice : {matrix.shape[0]} users × {matrix.shape[1]} products")
    print(f"Valeurs non-NaN : {matrix.notna().sum().sum()}")
    print(f"Sparsité : {matrix.isna().sum().sum() / matrix.size * 100:.2f}%")

    # Stats sur les produits par user
    products_per_user = matrix.notna().sum(axis=1)
    print(f"\n--- Produits par user ---")
    print(f"Moyenne : {products_per_user.mean():.1f}")
    print(f"Médiane : {products_per_user.median():.1f}")
    print(f"Q1 (25%): {products_per_user.quantile(0.25):.1f}")
    print(f"Max     : {products_per_user.max()}")

    # Prend le user avec le plus de produits notés
    test_user = products_per_user.idxmax()

    print(f"\nUser testé : {test_user}")
    print(f"Produits notés par ce user : {products_per_user[test_user]}")

    similar, error = get_similar_users(matrix, test_user, k=10)
    if error:
        print(f"Erreur : {error}")
    else:
        print(f"Users similaires :")
        print(similar)

    # Test recommandation
    print(f"\n--- Recommandations ---")
    recommendations, error = recommend(matrix, test_user, k=10, n=5)
    if error:
        print(f"Erreur : {error}")
    else:
        print(f"Top 5 produits recommandés :")
        for product_id, score in recommendations.items():
            print(f"  {product_id} : {score:.2f}")
