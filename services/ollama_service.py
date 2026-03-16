"""
Service de connexion à Ollama pour :
- Génération de descriptions produits
- Génération d'embeddings

Ollama doit tourner en local : ollama serve
"""

import requests

OLLAMA_URL = "http://localhost:11434"


CATEGORIES = [
    "Electronique",
    "Maison",
    "Beaute",
    "Alimentation",
    "Vetements",
    "Sport"
]


def generate_description(product_name: str, reviews: list[str] = None, model: str = "mistral") -> str:
    """
    Génère une description factuelle à partir du nom produit et des reviews

    Args:
        product_name: Nom du produit (souvent SEO/marketing)
        reviews: Liste des reviews clients (optionnel)
        model: Modèle Ollama à utiliser (mistral, llama2, phi, etc.)

    Returns:
        Description factuelle en 1-2 phrases
    """
    reviews_text = ""
    if reviews and len(reviews) > 0:
        # Prendre max 3 reviews pour pas surcharger
        sample_reviews = reviews[:3]
        reviews_text = f"\n\nAvis clients:\n" + "\n".join(f"- {r}" for r in sample_reviews)

    prompt = f"""Décris ce produit en 1-2 phrases factuelles.
Commence par le nom du produit, puis décris-le.
Utilise les avis UNIQUEMENT pour identifier:
- Le type exact de produit
- Ses caractéristiques techniques
- Son utilisation principale

N'inclus PAS: opinions, problèmes signalés, avis positifs/négatifs.

Produit: {product_name}{reviews_text}

Description:"""

    try:
        res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        res.raise_for_status()
        return res.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        print("Erreur: Ollama n'est pas lancé. Lance 'ollama serve' dans un terminal.")
        return None
    except Exception as e:
        print(f"Erreur génération description: {e}")
        return None


def categorize_product(product_name: str, description: str = None, model: str = "mistral") -> str:
    """
    Catégorise un produit parmi les catégories définies

    Args:
        product_name: Nom du produit
        description: Description générée (optionnel)
        model: Modèle Ollama

    Returns:
        Une catégorie parmi CATEGORIES
    """
    categories_str = ", ".join(CATEGORIES)
    desc_text = f"\nDescription: {description}" if description else ""

    prompt = f"""Catégorise ce produit dans UNE SEULE des catégories suivantes: {categories_str}

Produit: {product_name}{desc_text}

Réponds avec uniquement le nom de la catégorie, rien d'autre.
Catégorie:"""

    try:
        res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        res.raise_for_status()
        response = res.json()["response"].strip()

        # Nettoyer et valider la réponse
        for cat in CATEGORIES:
            if cat.lower() in response.lower():
                return cat
        return "Autre"
    except Exception as e:
        print(f"Erreur catégorisation: {e}")
        return None


def generate_tags(product_name: str, description: str = None, model: str = "mistral") -> list[str]:
    """
    Génère 3 mots-clés pour recherche d'image (Unsplash)

    Args:
        product_name: Nom du produit
        description: Description générée (optionnel)
        model: Modèle Ollama

    Returns:
        Liste de 3 mots-clés en anglais (pour Unsplash)
    """
    desc_text = f"\nDescription: {description}" if description else ""

    prompt = f"""You are helping find a stock photo for an e-commerce product.
Give exactly 3 GENERIC English words that describe what this product LOOKS like visually.

Rules:
- Use simple, common nouns (e.g. "bottle", "cream", "brush", "headphones")
- NO brand names
- NO words like "image", "photo", "product", "unsplash"
- NO adjectives, only nouns
- Think: what would I search on a stock photo site?

Product: {product_name}{desc_text}

Reply with ONLY 3 words separated by commas.
Example: bottle, skincare, serum
Keywords:"""

    try:
        res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        res.raise_for_status()
        response = res.json()["response"].strip()

        # Parser la réponse (format: "word1, word2, word3")
        tags = [t.strip().lower() for t in response.split(",")]
        # Garder seulement les 3 premiers mots valides
        tags = [t for t in tags if t and len(t) > 1][:3]

        return tags if len(tags) >= 1 else None
    except Exception as e:
        print(f"Erreur génération tags: {e}")
        return None


def get_embedding(text: str, model: str = "nomic-embed-text") -> list[float]:
    """
    Génère l'embedding vectoriel d'un texte

    Args:
        text: Texte à vectoriser
        model: Modèle d'embedding (nomic-embed-text recommandé)

    Returns:
        Liste de floats (768 dimensions pour nomic-embed-text)
    """
    try:
        res = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={
                "model": model,
                "prompt": text
            },
            timeout=30
        )
        res.raise_for_status()
        return res.json()["embedding"]
    except requests.exceptions.ConnectionError:
        print("Erreur: Ollama n'est pas lancé. Lance 'ollama serve' dans un terminal.")
        return None
    except Exception as e:
        print(f"Erreur génération embedding: {e}")
        return None


def check_ollama_status() -> bool:
    """Vérifie si Ollama est accessible"""
    try:
        res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return res.status_code == 200
    except:
        return False


def list_models() -> list[str]:
    """Liste les modèles disponibles dans Ollama"""
    try:
        res = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        res.raise_for_status()
        models = res.json().get("models", [])
        return [m["name"] for m in models]
    except:
        return []


# --- Test ---
if __name__ == "__main__":
    print("=== Test Ollama Service ===\n")

    # Check status
    if not check_ollama_status():
        print("Ollama n'est pas accessible.")
        print("Lance 'ollama serve' dans un terminal.")
        exit(1)

    print("Ollama OK")
    print(f"Modeles disponibles: {list_models()}\n")

    # Test description avec reviews
    test_name = "TOZO T6 True Wireless Earbuds Bluetooth 5.3 Headphones Touch Control with Wireless Charging Case IPX8 Waterproof"
    test_reviews = [
        "Great sound quality for the price, very comfortable",
        "Battery life is amazing, lasts all day",
        "Bass could be better but overall good value"
    ]

    print(f"Nom produit:\n{test_name}\n")
    print(f"Reviews:\n{test_reviews}\n")

    desc = generate_description(test_name, test_reviews)
    if desc:
        print(f"Description generee:\n{desc}\n")

        # Test catégorisation
        cat = categorize_product(test_name, desc)
        print(f"Categorie: {cat}\n")

        # Test embedding (si modele dispo)
        emb = get_embedding(desc)
        if emb:
            print(f"Embedding: {len(emb)} dimensions")
            print(f"Premiers 5 valeurs: {emb[:5]}")
        else:
            print("Embedding: modele nomic-embed-text non installe")
            print("Fais: ollama pull nomic-embed-text")
