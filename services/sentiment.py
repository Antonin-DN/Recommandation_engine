# divergence = abs(rating - sentiment)

# Si divergence faible → moyenne simple
# Si divergence forte → privilégie le sentiment
"""
weight_sentiment = min(1.0, 0.5 + divergence / 5.0)
weight_rating = 1.0 - weight_sentiment

adjusted_score = (weight_sentiment * sentiment) + (weight_rating * rating)
```

**Exemple 1 : Accord fort**
```
Rating : 5/5
Sentiment : 4.8/5
Divergence : 0.2

weight_sentiment = 0.5 + 0.2/5 = 0.54
weight_rating = 0.46

adjusted_score = 0.54 * 4.8 + 0.46 * 5 = 4.89
→ Moyenne quasi normale car ils sont d'accord
```

**Exemple 2 : Conflit fort**
```
Rating : 5/5
Sentiment : 1.2/5
Divergence : 3.8

weight_sentiment = 0.5 + 3.8/5 = 1.26 → cap à 1.0
weight_rating = 0.0

adjusted_score = 1.0 * 1.2 + 0.0 * 5 = 1.2
→ On fait 100% confiance au sentiment
```

**Exemple 3 : Conflit modéré**
```
Rating : 4/5
Sentiment : 2.5/5
Divergence : 1.5

weight_sentiment = 0.5 + 1.5/5 = 0.8
weight_rating = 0.2

adjusted_score = 0.8 * 2.5 + 0.2 * 4 = 2.8
→ On privilégie le sentiment mais le rating compte un peu
"""
# Suggestion Claude code
""""
  1. Ce que TextBlob retourne

  TextBlob("This product is amazing").sentiment.polarity  # → 0.75
  TextBlob("Terrible quality").sentiment.polarity          # → -1.0

  Un float entre -1 (très négatif) et +1 (très positif). Ton rating est entre 1 et 5. Il faut convertir la polarité sur
  la même échelle :

  # Convertir polarity [-1, +1] → sentiment_rating [1, 5]
  sentiment_rating = 1 + (polarity + 1) * 2
  # -1 → 1, 0 → 3, +1 → 5

  2. Filtrer les commentaires hors-produit (livraison, etc.)

  C'est faisable mais attention — c'est un sujet complexe en NLP. Deux approches :

  - Simple : une liste de mots-clés à exclure (shipping, delivery, packaging, arrived). Si le commentaire contient
  majoritairement ces mots, on l'ignore pour le sentiment et on garde le rating brut.
  - Avancé : Aspect-Based Sentiment Analysis (librairie spaCy ou modèles transformers). Overkill pour ton projet.

  Je recommande l'approche simple avec mots-clés.

  3. Pondération variable selon l'écart rating/sentiment

  C'est ta meilleure idée. Le principe :

  écart = |rating - sentiment_rating|    (sur l'échelle 1-5)
  écart_max = 4                          (différence max possible : 5 - 1)

  # Plus l'écart est grand, plus le sentiment prend le dessus
  sentiment_weight = écart / écart_max   (entre 0 et 1)

  adjusted_rating = (1 - sentiment_weight) * rating + sentiment_weight * sentiment_rating

  Exemples concrets :
  ┌────────┬───────────┬───────┬─────────────────┬───────────────────────────────────┐
  │ Rating │ Sentiment │ Écart │ Poids sentiment │          adjusted_rating          │
  ├────────┼───────────┼───────┼─────────────────┼───────────────────────────────────┤
  │ 5      │ 4.5       │ 0.5   │ 0.125           │ ~4.94 (presque pas de correction) │
  ├────────┼───────────┼───────┼─────────────────┼───────────────────────────────────┤
  │ 5      │ 1.5       │ 3.5   │ 0.875           │ ~1.94 (sentiment domine)          │
  ├────────┼───────────┼───────┼─────────────────┼───────────────────────────────────┤
  │ 2      │ 4.0       │ 2.0   │ 0.5             │ 3.0 (50/50)                       │
  └────────┴───────────┴───────┴─────────────────┴───────────────────────────────────┘
  Ça correspond exactement à ce que tu voulais : proche → le sentiment change rien, loin → le sentiment prend le dessus.

  Résumé du flux dans sentiment.py

  1. TextBlob(review) → polarity [-1, +1]
  2. Convertir en sentiment_rating [1, 5]
  3. Filtrer les mots hors-produit (optionnel)
  4. Calculer l'écart rating vs sentiment
  5. Pondérer → adjusted_rating
"""
total = len(df)
keywords = ['shipping', 'delivery', 'delivered', 'packaging', 'arrived', 'package', 'shipped']
for word in keywords:
    count = df['Reviews'].str.lower().str.contains(word).sum()
    print(f'{word}: {count} ({round(count/total*100, 2)}%%)')
print(f'\nTotal lignes: {total}')
   