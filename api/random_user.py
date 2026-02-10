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
    user_history = df[df["UserId"] == user_id][["ProductId", "product_name", "Rating", "Reviews", "Timestamp"]]

    # Génère un nom aléatoire
    fake_name = fake.name()

    return {
        "user_id": user_id,
        "name": fake_name,
        "nb_products": len(user_history),
        "history": user_history.to_dict(orient="records")
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
        review = item['Reviews'][:50] + "..." if len(item['Reviews']) > 50 else item['Reviews']
        print(f"  - {item['product_name'][:40]}")
        print(f"    Rating: {item['Rating']} | Commentaire: {review}")
        print()
