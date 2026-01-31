"""t_min = date de la review la plus ancienne du dataset
t_max = date de la review la plus récente du dataset
t_reference = t_max + 1 jour  # Ton "jour J"

poids = 1 - (distance_review / distance_totale)

la valeur de la note est pondéré en fonction de la date.

min_weight = 0.7
max_weight = 1.0

# Fonction de transformation
def rescale(x, min_w=0.7, max_w=1.0):
    return min_w + (max_w - min_w) * x

# Exemples
print("Original → Rescalé")

Effet 1 : Impact sur les notes d'un MÊME produitSi un produit a des reviews à différentes périodes, les notes récentes pèsent plus lourd
enfaite je me dit pour l'effet 2 si un produit est evergreen il aura aussi des review recente donc en soi la ponderation n'a pas d'impact si les review reste stable sur le long therme, ce que je voudrais c'est entre 2 produit différent mais proche admettons si un a etait acheter il y a plus longtemps que l'autre à note egale le plus recent passe devant et 2 si le meme produit voit ses notes degradé les notes les plus recente ont plus d'impact (ou inversement) pour corrigé plus vite les recommandations, exemple un fournisseur baisse sa qualité et s'appuie sur sa notoriété pour continuer de vendre
Système de recommandation avec 3 niveaux d'intelligence temporelle :
    
    1. Pondération des reviews individuelles [0.7, 1.0]
       → Les notes récentes d'un produit comptent plus
    
    2. Score de récence par produit (tie-breaker)
       → Entre 2 produits similaires, favorise le plus récent
    
    3. Détection de tendances (pénalités)
       → Pénalise les produits dont la qualité se dégrade
    """