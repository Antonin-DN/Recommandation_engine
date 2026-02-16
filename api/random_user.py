import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from services.data_loader import load_and_clean


def get_random_user(df):
    """Sélectionne un user aléatoire et retourne ses infos"""

    fake = Faker()

    # Sélectionne un userId aléatoire
    user_id = random.choice(df["UserId"].unique())

    # Récupère l'historique de ce user
    user_history = df[df["UserId"] == user_id][["ProductId", "product_name", "Rating", "Reviews", "Timestamp"]].copy()

    # Ajoute une colonne date (sans l'heure) pour grouper
    user_history["Date"] = user_history["Timestamp"].dt.date

    # Groupe par ProductId + Date pour avoir la quantité
    grouped = user_history.groupby(["ProductId", "Date"]).agg({
        "product_name": "first",
        "Rating": "mean",  # moyenne si plusieurs ratings
        "Timestamp": "first"
    }).reset_index()

    # Compte la quantité (nombre de lignes par groupe)
    quantity = user_history.groupby(["ProductId", "Date"]).size().reset_index(name="quantity")
    grouped = grouped.merge(quantity, on=["ProductId", "Date"])

    # Génère un nom aléatoire
    fake_name = fake.name()

    # Construit l'historique
    history = []
    for _, row in grouped.iterrows():
        history.append({
            "ProductId": row["ProductId"],
            "product_name": row["product_name"],
            "Rating": row["Rating"],
            "Timestamp": row["Timestamp"],
            "quantity": int(row["quantity"])
        })

    return {
        "user_id": user_id,
        "name": fake_name,
        "nb_products": len(history),
        "history": history
    }


# --- Test ---
if __name__ == "__main__":
    df, is_clean = load_and_clean("data/Group6.xlsx")

    user = get_random_user(df)
    print(f"User ID : {user['user_id']}")
    print(f"Nom     : {user['name']}")
    print(f"Produits achetés : {user['nb_products']}")
    print(f"\nHistorique :")
    for item in user["history"]:
        print(f"  - {item['product_name'][:40]}")
        print(f"    Rating: {item['Rating']} | Qté: {item['quantity']}")
        print()
