"""
Test complet du workflow de recommandation
Exécute le pipeline et affiche les DataFrames pour vérification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.data_loader import load_and_clean, get_products_df
from services.sentiment import analyze_sentiment, convert_polarity_to_rating, compute_adjusted_rating
from services.time_weighting import apply_time_weight
from models.user_based import build_matrix, recommend


print("=" * 60)
print("ÉTAPE 1 : Chargement du dataset")
print("=" * 60)

df, is_clean = load_and_clean("data/Group6.xlsx")
print(f"Entrées : {len(df)}")
print(f"Clean : {is_clean}")
print(f"\nColonnes de base : {list(df.columns)}")


print("\n" + "=" * 60)
print("ÉTAPE 2 : Enrichissement sentiment")
print("=" * 60)

df = analyze_sentiment(df)
df = convert_polarity_to_rating(df)
df = compute_adjusted_rating(df)

print(f"Colonnes après sentiment : {list(df.columns)}")
print(f"\nAperçu df enrichi :")
print(df[["UserId", "ProductId", "Rating", "polarity", "sentiment_rating", "adjusted_rating"]].head(10).to_string())


print("\n" + "=" * 60)
print("ÉTAPE 3 : Pondération temporelle (optionnel)")
print("=" * 60)

df = apply_time_weight(df)
print(f"Colonnes après time_weight : {list(df.columns)}")
print(f"\nAperçu avec weighted_rating :")
print(df[["Timestamp", "adjusted_rating", "weighted_rating"]].head(5).to_string())


print("\n" + "=" * 60)
print("ÉTAPE 4 : DataFrame produits agrégé")
print("=" * 60)

# On recharge le df original pour products_df (sans enrichissement sentiment)
df_original, _ = load_and_clean("data/Group6.xlsx")
products_df = get_products_df(df_original)

print(f"Entrées products_df : {len(products_df)}")
print(f"Colonnes : {list(products_df.columns)}")
print(f"\nAperçu products_df :")
print(products_df.head(10).to_string())


print("\n" + "=" * 60)
print("ÉTAPE 5 : Matrice User × Product")
print("=" * 60)

matrix = build_matrix(df)
print(f"Shape : {matrix.shape[0]} users × {matrix.shape[1]} products")
print(f"Sparsité : {matrix.isna().sum().sum() / matrix.size * 100:.2f}%")


print("\n" + "=" * 60)
print("ÉTAPE 6 : Test recommandation User-Based")
print("=" * 60)

# Prend un user avec beaucoup de produits pour le test
products_per_user = matrix.notna().sum(axis=1)
test_user = products_per_user.idxmax()

print(f"User testé : {test_user}")
print(f"Produits notés : {products_per_user[test_user]}")

recommendations, error = recommend(matrix, test_user, k=10, n=5)
if error:
    print(f"Erreur : {error}")
else:
    print(f"\nTop 5 recommandations :")
    for product_id, score in recommendations.items():
        # Récupère le nom du produit
        name = products_df[products_df["ProductId"] == product_id]["product_name"].values
        name = name[0][:50] if len(name) > 0 else "N/A"
        print(f"  {product_id[:15]} | {score:.2f} | {name}")


print("\n" + "=" * 60)
print("RÉSUMÉ")
print("=" * 60)
print(f"""
df (commandes)      : {len(df)} entrées
products_df         : {len(products_df)} produits uniques
matrix              : {matrix.shape[0]} users × {matrix.shape[1]} products

Colonnes df enrichi :
  - polarity         : sentiment [-1, +1]
  - sentiment_rating : converti [1, 5]
  - adjusted_rating  : moyenne pondérée rating + sentiment
  - weighted_rating  : ajusté par le temps

Colonnes products_df :
  - ProductId
  - product_name
  - avg_rating
  - review_count
""")
