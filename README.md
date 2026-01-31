User-Based Collaborative Filtering (le plus simple)
Item-Based Collaborative Filtering (symétrique du user-based)
Matrix Factorization (SVD) (plus puissant)
SVD avec pondération temporelle (le plus sophistiqué)

Résumé dépendances
  ┌───────────────────┬─────────────────────┬───────────────────────────┐
  │      Brique       │      Approche       │            Lib            │
  ├───────────────────┼─────────────────────┼───────────────────────────┤
  │ Sentiment         │ Librairie           │ textblob                  │
  ├───────────────────┼─────────────────────┼───────────────────────────┤
  │ Pondération temps │ Hardcode            │ pandas (dates)            │
  ├───────────────────┼─────────────────────┼───────────────────────────┤
  │ User-based        │ Hardcode            │ pandas + numpy            │
  ├───────────────────┼─────────────────────┼───────────────────────────┤
  │ Item-based        │ Hardcode + 1 helper │ sklearn.cosine_similarity │
  ├───────────────────┼─────────────────────┼───────────────────────────┤
  │ SVD               │ Hardcode            │ numpy.linalg.svd          │