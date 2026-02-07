def apply_time_weight(df, min_weight=0.7, max_weight=1.0):
    """Pondère le adjusted_rating en fonction de la date de la review"""

    t_min = df["Timestamp"].min()
    t_max = df["Timestamp"].max()
    spread = (t_max - t_min).days  # nombre de jours entre la plus ancienne et la plus récente

    # Distance en jours depuis la review la plus ancienne
    days_from_min = (df["Timestamp"] - t_min).dt.days

    # Ratio entre 0 (plus ancienne) et 1 (plus récente)
    ratio = days_from_min / spread

    # Poids entre min_weight et max_weight
    weight = min_weight + (max_weight - min_weight) * ratio

    # Applique le poids au adjusted_rating
    df["weighted_rating"] = df["adjusted_rating"] * weight

    return df


# --- Test ---
if __name__ == "__main__":
    from data_loader import load_and_clean
    from sentiment import analyze_sentiment, convert_polarity_to_rating, compute_adjusted_rating

    df, is_clean = load_and_clean("data/Group6.xlsx")
    df = analyze_sentiment(df)
    df = convert_polarity_to_rating(df)
    df = compute_adjusted_rating(df)
    df = apply_time_weight(df)

    print(df[["Timestamp", "Rating", "adjusted_rating", "weighted_rating"]].head(10))
    print()
    print(f"Min weighted_rating : {df['weighted_rating'].min():.3f}")
    print(f"Max weighted_rating : {df['weighted_rating'].max():.3f}")
