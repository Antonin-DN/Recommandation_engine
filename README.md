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


  Chose à rajouter dans data loader : 
  - Moyenne global de tout les avis et nombres d'avis au data frame, prix random 

  API :
  Une route pour générer un profil user random dans le dataset, on selectionne un puis on récupère son historique de commande
  Une route pour générer la recommandation basée sur le modèle
  Les photos a voir en fonction du nombre de produit (count distinct)

Min : 2003-01-11 07:45:02
Max : 2023-05-15 04:47:27
Users distincts : 7023
Produits distincts : 8623

