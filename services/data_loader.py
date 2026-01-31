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


# --- Code de test (exécuté uniquement en direct) ---
if __name__ == "__main__":
    df, is_clean = load_and_clean("data/Group6.xlsx")
    print(df.head())
    print(f"Clean : {is_clean}")
