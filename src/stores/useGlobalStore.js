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

  // Produits recommandés (populaires par défaut)
  recommendedProducts: [],

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
  setModel: (model) => set({ model }),

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

      set({ user, isConnected: true, model: "user-based" })
    } catch (err) {
      console.error('Erreur chargement user:', err)
    }
  },

  // Charge un user par son ID
  loadUserById: async (userId) => {
    // TODO: remplacer par fetch(`/api/user/${userId}`)
    const mockUser = {
      id: userId,
      name: "User " + userId.substring(0, 4),
      avatar: userId.substring(0, 2).toUpperCase(),
      orders: [
        { productId: 2, date: "2024-03-01", rating: 4.0 },
        { productId: 4, date: "2024-02-15", rating: 3.5 },
      ]
    }
    set({ user: mockUser, isConnected: true, model: "user-based" })
  },

  // Reset user
  clearUser: () => set({
    user: null,
    isConnected: false,
    model: "popular",
    showHistory: false,
  }),

  // --- Actions Recommendations ---

  // Charge les recommandations selon le modèle
  fetchRecommendations: async () => {
    // TODO: const { model, user } = get()
    // const products = await fetch('/api/recommendations', { model, userId: user?.id })
    // set({ recommendedProducts: products })
  },
}))

export default useGlobalStore
