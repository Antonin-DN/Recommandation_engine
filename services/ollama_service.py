"""
Service de connexion à Ollama pour :
- Génération de descriptions produits
- Génération d'embeddings

Ollama doit tourner en local : ollama serve
"""

import requests

OLLAMA_URL = "http://localhost:11434"


def generate_description(product_name: str, model: str = "mistral") -> str:
    """
    Génère une description claire à partir du nom produit marketing

    Args:
        product_name: Nom du produit (souvent SEO/marketing)
        model: Modèle Ollama à utiliser (mistral, llama2, phi, etc.)

    Returns:
        Description claire en 1-2 phrases
    """
    prompt = f"""Tu es un assistant qui décrit des produits de manière claire et concise.
À partir du nom de produit suivant, génère une description simple en 1-2 phrases.
Ne répète pas le nom complet, extrais juste l'essentiel.

Nom du produit: {product_name}

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

    # Test description
    test_name = "TOZO T6 True Wireless Earbuds Bluetooth 5.3 Headphones Touch Control with Wireless Charging Case IPX8 Waterproof"
    print(f"Nom produit:\n{test_name}\n")

    desc = generate_description(test_name)
    if desc:
        print(f"Description generee:\n{desc}\n")

        # Test embedding
        emb = get_embedding(desc)
        if emb:
            print(f"Embedding: {len(emb)} dimensions")
            print(f"Premiers 5 valeurs: {emb[:5]}")
