import pandas as pd
from textblob import TextBlob


def analyze_sentiment(df):
    """Analyse le sentiment des reviews et retourne le df avec une colonne polarity"""

    # Applique TextBlob sur chaque review, retourne la polarité [-1, +1]
    df["polarity"] = df["Reviews"].apply(lambda x: TextBlob(x).sentiment.polarity) #tester Vader nltk 

    return df


def convert_polarity_to_rating(df):
    """Convertit la polarité [-1, +1] en sentiment_rating [1, 5]"""

    df["sentiment_rating"] = 1 + (df["polarity"] + 1) * 2

    return df


def compute_adjusted_rating(df):
    """Pondère entre Rating et sentiment_rating en fonction de l'écart"""

    # Écart entre le rating et le sentiment (entre 0 et 4)
    ecart = abs(df["Rating"] - df["sentiment_rating"])
    # Intéressant de checker le plus gros écart pour voir

    # Plus l'écart est grand, plus le sentiment prend le dessus (max 80%)
    sentiment_weight = (ecart / 4) * 0.8 # formule linéaire pour un écart max de 4, pondérage max 80% sentiement car non neutre et prend l'avantage sur rating.
    rating_weight = 1 - sentiment_weight

    df["adjusted_rating"] = rating_weight * df["Rating"] + sentiment_weight * df["sentiment_rating"]

    return df


# --- Test : distribution des polarités ---
if __name__ == "__main__":
    import pandas as pd
    from data_loader import load_and_clean

    df, is_clean = load_and_clean("data/Group6.xlsx")
    df = analyze_sentiment(df)
    df = convert_polarity_to_rating(df)
    df = compute_adjusted_rating(df)
    print(df[["Rating", "polarity", "sentiment_rating", "adjusted_rating"]].head(10))
"""""
    print("--- Distribution des polarités ---")
    print(f"Min     : {df['polarity'].min()}")
    print(f"Max     : {df['polarity'].max()}")
    print(f"Moyenne : {df['polarity'].mean():.3f}")
    print(f"Médiane : {df['polarity'].median():.3f}")
    print()
    print("--- Comptage par catégorie ---")
    print(f"Très négatif [-1, -0.6]  : {len(df[df['polarity'] <= -0.6])}")
    print(f"Négatif      [-0.6, -0.2]: {len(df[(df['polarity'] > -0.6) & (df['polarity'] <= -0.2)])}")
    print(f"Neutre       [-0.2, 0.2] : {len(df[(df['polarity'] > -0.2) & (df['polarity'] <= 0.2)])}")
    print(f"Positif      [0.2, 0.6]  : {len(df[(df['polarity'] > 0.2) & (df['polarity'] <= 0.6)])}")
    print(f"Très positif [0.6, 1]    : {len(df[df['polarity'] > 0.6])}")
"""
