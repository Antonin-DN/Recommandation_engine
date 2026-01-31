# =============================================================================
# MOTEUR DE RECOMMANDATION
# =============================================================================

# STEP 1: Import & Load Data
# - Charger le fichier xlsx (Group1.xlsx)
# - Colonnes attendues: user_id, product_id, rating, comment

# STEP 2: Sentiment Analysis
# - Analyser le sentiment de chaque commentaire (TextBlob)
# - Score sentiment: -1 (négatif) à +1 (positif)

# STEP 3: Score Pondéré
# - Combiner rating + sentiment pour créer un score pondéré
# - Formule: score = rating * (1 + sentiment * weight)

# STEP 4: Matrice User-Product
# - Créer une matrice users (lignes) x products (colonnes)
# - Valeurs = scores pondérés

# STEP 5: Similarité Users
# - Calculer corrélation entre users (Pearson ou Cosine)
# - Trouver les K users les plus similaires à l'user cible

# STEP 6: Recommandations
# - Identifier produits achetés par users similaires
# - Exclure produits déjà achetés par l'user cible
# - Calculer moyenne pondérée des scores
# - Retourner top N produits avec meilleure moyenne

# =============================================================================
# 3 MODÈLES DE RECOMMANDATION
# =============================================================================
#
# 1. USER-BASED COLLABORATIVE FILTERING
#    - Trouve des users avec des goûts similaires (corrélation Pearson)
#    - Recommande ce que les users similaires ont aimé
#    - Simple mais sensible au cold start
#
# 2. ITEM-BASED COLLABORATIVE FILTERING
#    - Trouve des produits similaires (achetés par les mêmes users)
#    - "Les gens qui ont aimé X ont aussi aimé Y"
#    - Plus stable, les relations produits changent moins
#
# 3. MATRIX FACTORIZATION (SVD)
#    - Décompose la matrice user-product en facteurs latents
#    - Capture des patterns cachés (ex: "aime le style minimaliste")
#    - Plus précis, gère mieux les données sparse
#    - Utilisé par Netflix
#
# =============================================================================
