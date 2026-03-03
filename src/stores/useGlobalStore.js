import { create } from 'zustand'

/*
Structure des données:

user: {
  id: "A2SUAM1J3GNN3B",
  name: "Lucas M.",
  avatar: "LM",
  orders: [
    { productId: "B001E4KFG0", date: "2024-03-15", rating: 4.5 },
    { productId: "B00813GRG4", date: "2024-02-20", rating: 3.0 },
  ]
}

recommendedProducts: [
  {
    id: "B001E4KFG0",
    name: "Casque Audio Pro",
    category: "Electronics",
    price: 89.99,
    rating: 4.3,
    reviewCount: 1247,
    image: "https://..."
  },
]

modelStats: {
  precision: 0.82,
  recall: 0.75,
  // etc - à définir plus tard
}
*/

const useGlobalStore = create((set, get) => ({
  // User
  user: null,
  isConnected: false,

  // Produits recommandés
  recommendedProducts: [],
  popularProducts: null, // Cache permanent pour les produits populaires
  recommendationError: null, // Erreur de recommandation (ex: pas assez de commandes)

  // Recherche sémantique
  searchResults: null, // null = pas en mode recherche, [] = recherche vide
  searchQuery: "",

  // Produits similaires (modal)
  selectedProduct: null,
  similarProducts: [],

  // Modèle actif
  model: "popular",

  // Stats du modèle (plus tard)
  modelStats: null,

  // UI
  showHistory: false,
  showLogin: false,
  modelDropdown: false,

  // --- Actions UI ---
  setShowHistory: (show) => set({ showHistory: show }),
  setShowLogin: (show) => set({ showLogin: show }),
  setModelDropdown: (show) => set({ modelDropdown: show }),

  // --- Actions Model ---
  setModel: (model) => {
    set({ model })
    // Fetch les nouvelles recommandations quand on change de modèle
    get().fetchRecommendations()
  },

  // --- Actions User ---

  // Génère un user random (appel API)
  generateRandomUser: async () => {
    try {
      const res = await fetch('/api/user/random')
      const data = await res.json()

      // Transforme la réponse API au format frontend
      const user = {
        id: data.user_id,
        name: data.name,
        avatar: data.name.split(' ').map(n => n[0]).join('').toUpperCase(),
        orders: data.history.map(h => ({
          productId: h.ProductId,
          productName: h.product_name,
          rating: h.Rating,
          date: h.Timestamp?.split('T')[0] || h.Timestamp,
          quantity: h.quantity || 1,
        }))
      }

      // Reste sur popular, ne change pas de modèle automatiquement
      set({ user, isConnected: true })
    } catch (err) {
      console.error('Erreur chargement user:', err)
    }
  },

  // Charge un user par son ID
  loadUserById: async (userId) => {
    try {
      const res = await fetch(`/api/user/${userId}`)
      const data = await res.json()

      if (data.error) {
        console.error('User non trouve:', data.error)
        return false
      }

      const user = {
        id: data.user_id,
        name: data.name,
        avatar: data.name.split(' ').map(n => n[0]).join('').toUpperCase(),
        orders: data.history.map(h => ({
          productId: h.ProductId,
          productName: h.product_name,
          rating: h.Rating,
          date: h.Timestamp?.split('T')[0] || h.Timestamp,
          quantity: h.quantity || 1,
        }))
      }

      set({ user, isConnected: true })
      return true
    } catch (err) {
      console.error('Erreur chargement user:', err)
      return false
    }
  },

  // Reset user
  clearUser: () => {
    set({
      user: null,
      isConnected: false,
      model: "popular",
      showHistory: false,
    })
    // Recharge les produits populaires
    get().fetchRecommendations()
  },

  // --- Actions Recommendations ---

  // Charge les recommandations selon le modèle
  fetchRecommendations: async () => {
    const { model, user, popularProducts } = get()

    // Reset l'erreur
    set({ recommendationError: null })

    // Pour popular : utilise le cache si dispo
    if (model === "popular" && popularProducts) {
      set({ recommendedProducts: popularProducts })
      return
    }

    try {
      const params = new URLSearchParams({
        model: model,
        n: '10'
      })

      if (user?.id) {
        params.append('user_id', user.id)
      }

      const res = await fetch(`/api/recommendations?${params}`)
      const data = await res.json()

      if (data.error) {
        console.error('Erreur API:', data.error)
        set({ recommendationError: data.error, recommendedProducts: [] })
        return
      }

      // Cache les produits populaires
      if (model === "popular") {
        set({ recommendedProducts: data.products, popularProducts: data.products })
      } else {
        set({ recommendedProducts: data.products })
      }
    } catch (err) {
      console.error('Erreur chargement recommendations:', err)
      set({ recommendationError: 'Erreur de connexion au serveur' })
    }
  },

  // --- Actions Search ---
  setSearchResults: (results, query) => {
    set({ searchResults: results, searchQuery: query })
  },

  clearSearch: () => {
    set({ searchResults: null, searchQuery: "" })
  },

  // --- Actions Similar Products ---
  fetchSimilarProducts: async (product) => {
    set({ selectedProduct: product, similarProducts: [] })
    try {
      const res = await fetch(`/api/similar/${product.id}?n=6`)
      const data = await res.json()
      if (data.similar) {
        const products = data.similar.map(p => ({
          id: p.product_id,
          name: p.name,
          description: p.description,
          category: p.category,
          rating: p.avg_rating || 4.0,
          reviewCount: p.review_count || 0,
          price: Math.round((Math.random() * 200 + 10) * 100) / 100,
          image: `https://picsum.photos/seed/${p.product_id}/300/300`,
          similarity: p.similarity
        }))
        set({ similarProducts: products })
      }
    } catch (err) {
      console.error("Erreur similar products:", err)
    }
  },

  closeSimilarProducts: () => {
    set({ selectedProduct: null, similarProducts: [] })
  },
}))

export default useGlobalStore
