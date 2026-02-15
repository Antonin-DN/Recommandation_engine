// Données mock pour le développement - sera remplacé par l'API

export const MODEL_LABELS = {
  "popular": { name: "Plus Populaires" },
  "user-based": { name: "User-Based CF" },
  "item-based": { name: "Item-Based CF" },
  "svd": { name: "SVD" },
}

// Mock products - sera remplacé par l'API /api/products/popular
export const products = [
  { id: 1, name: "Écouteurs Bluetooth Pro", category: "Électronique", price: 89.99, rating: 4.5, reviewCount: 1247, image: "https://images.unsplash.com/photo-1590658268037-6bf12f032f55?w=400&h=400&fit=crop", popularity: 95 },
  { id: 2, name: "Chargeur Sans Fil 15W", category: "Électronique", price: 29.99, rating: 4.2, reviewCount: 856, image: "https://images.unsplash.com/photo-1615526675159-e248c3021d3f?w=400&h=400&fit=crop", popularity: 88 },
  { id: 3, name: "Clavier Mécanique RGB", category: "Électronique", price: 149.99, rating: 4.8, reviewCount: 2103, image: "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=400&fit=crop", popularity: 92 },
  { id: 4, name: "Lampe de Bureau LED", category: "Maison", price: 45.00, rating: 4.3, reviewCount: 654, image: "https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=400&h=400&fit=crop", popularity: 78 },
  { id: 5, name: "Tapis de Yoga", category: "Sport", price: 35.00, rating: 4.6, reviewCount: 1890, image: "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop", popularity: 85 },
  { id: 6, name: "Sneakers Urban", category: "Mode", price: 120.00, rating: 4.4, reviewCount: 967, image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop", popularity: 91 },
  { id: 7, name: "Data Science avec Python", category: "Livres", price: 42.00, rating: 4.7, reviewCount: 445, image: "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop", popularity: 82 },
  { id: 8, name: "Robot Multifonction", category: "Cuisine", price: 199.00, rating: 4.5, reviewCount: 1567, image: "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop", popularity: 89 },
  { id: 9, name: "Sérum Vitamine C", category: "Beauté", price: 28.00, rating: 4.4, reviewCount: 2234, image: "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=400&fit=crop", popularity: 87 },
  { id: 10, name: "Kit Herbes Aromatiques", category: "Jardin", price: 24.99, rating: 4.1, reviewCount: 389, image: "https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=400&h=400&fit=crop", popularity: 75 },
]
