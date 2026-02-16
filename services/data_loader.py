import pandas as pd


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
    - ProductId (index)
    - product_name
    - avg_rating (moyenne des notes)
    - review_count (nombre de reviews)
    """
    products_df = df.groupby("ProductId").agg(
        product_name=("product_name", "first"),
        avg_rating=("Rating", "mean"),
        review_count=("Rating", "count")
    ).reset_index()

    # Arrondir la moyenne à 1 décimale
    products_df["avg_rating"] = products_df["avg_rating"].round(1)

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
