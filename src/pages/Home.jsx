import { useEffect } from "react"
import { ShoppingBag, User as UserIcon, ChevronDown, Sparkles, TrendingUp, Cpu, Brain, BarChart3, LogOut, Search } from "lucide-react"
import ProductCard from "../components/ProductCard"
import OrderHistory from "../components/OrderHistory"
import LoginDialog from "../components/LoginDialog"
import SearchBar from "../components/SearchBar"
import SimilarProductsModal from "../components/SimilarProductsModal"
import useGlobalStore from "../stores/useGlobalStore"
import { MODEL_LABELS } from "../data/mockData"

const MODELS = ["popular", "user-based", "item-based", "svd"]

const MODEL_ICONS = {
  "popular": <TrendingUp className="w-4 h-4" />,
  "user-based": <Brain className="w-4 h-4" />,
  "item-based": <Cpu className="w-4 h-4" />,
  "svd": <BarChart3 className="w-4 h-4" />,
}

export default function Home() {
  const {
    user,
    isConnected,
    model,
    recommendedProducts,
    popularProducts,
    recommendationError,
    searchResults,
    searchQuery,
    showHistory,
    showLogin,
    modelDropdown,
    setModel,
    setShowHistory,
    setShowLogin,
    setModelDropdown,
    clearUser,
    fetchRecommendations,
    setSearchResults,
    clearSearch,
    selectedProduct,
    similarProducts,
    fetchSimilarProducts,
    closeSimilarProducts,
  } = useGlobalStore()

  // Mode recherche actif ?
  const isSearchMode = searchResults !== null

  // Produits à afficher : recherche > recommandés > popular
  const displayProducts = isSearchMode
    ? searchResults.map(r => ({
        id: r.product_id,
        name: r.name,
        description: r.description,
        category: r.category,
        rating: r.avg_rating || 4.0,
        reviewCount: r.review_count || 0,
        price: Math.round((Math.random() * 200 + 10) * 100) / 100,
        image: `https://picsum.photos/seed/${r.product_id}/300/300`,
        similarity: r.similarity
      }))
    : recommendedProducts.length > 0
      ? recommendedProducts
      : popularProducts || []

  // Charge les produits populaires au premier rendu
  useEffect(() => {
    fetchRecommendations()
  }, [])

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-primary">
        <div className="max-w-[1400px] mx-auto px-4 h-[52px] flex items-center gap-2">
          {/* Logo */}
          <div className="flex items-center gap-1.5 shrink-0 cursor-pointer" onClick={clearUser}>
            <Sparkles className="w-5 h-5 text-secondary" />
            <span className="font-extrabold text-lg tracking-tight text-primary-foreground">
              reco<span className="text-secondary">shop</span>
            </span>
          </div>

          <div className="w-px h-6 bg-primary-foreground/15 mx-2 hidden sm:block" />

          {/* Search Bar */}
          <div className="hidden lg:block flex-1 max-w-sm">
            <SearchBar
              onResults={(results, query) => setSearchResults(results, query)}
              onClear={clearSearch}
            />
          </div>

          <div className="w-px h-6 bg-primary-foreground/15 mx-2 hidden lg:block" />

          {/* Model tabs - desktop */}
          <nav className="hidden md:flex items-center gap-0.5">
            {MODELS.map((m) => (
              <button
                key={m}
                onClick={() => setModel(m)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium transition-all ${
                  m === model
                    ? "bg-secondary text-secondary-foreground"
                    : "text-primary-foreground/60 hover:text-primary-foreground hover:bg-primary-foreground/5"
                }`}
              >
                {MODEL_ICONS[m]}
                {MODEL_LABELS[m].name}
              </button>
            ))}
          </nav>

          {/* Model dropdown - mobile */}
          <div className="md:hidden relative">
            <button
              onClick={() => setModelDropdown(!modelDropdown)}
              className="flex items-center gap-2 px-3 py-1.5 rounded bg-primary-foreground/10 text-primary-foreground text-xs font-medium"
            >
              {MODEL_ICONS[model]}
              {MODEL_LABELS[model].name}
              <ChevronDown className={`w-3.5 h-3.5 transition-transform ${modelDropdown ? "rotate-180" : ""}`} />
            </button>
            {modelDropdown && (
              <>
                <div className="fixed inset-0 z-40" onClick={() => setModelDropdown(false)} />
                <div className="absolute left-0 top-full mt-1 w-56 bg-card rounded-lg shadow-2xl border border-border z-50 overflow-hidden">
                  {MODELS.map((m) => (
                    <button
                      key={m}
                      onClick={() => { setModel(m); setModelDropdown(false) }}
                      className={`w-full text-left px-3 py-2.5 flex items-center gap-2.5 text-xs hover:bg-muted transition-colors ${
                        m === model ? "bg-muted font-semibold" : ""
                      }`}
                    >
                      <span className={m === model ? "text-secondary" : "text-muted-foreground"}>
                        {MODEL_ICONS[m]}
                      </span>
                      <span className={m === model ? "text-secondary" : "text-card-foreground"}>
                        {MODEL_LABELS[m].name}
                      </span>
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>

          {/* Right section */}
          <div className="flex items-center gap-2 shrink-0 ml-auto">
            {isConnected && user ? (
              <div className="flex items-center gap-2">
                {/* Profil */}
                <div className="flex items-center gap-2 px-2 py-1 rounded-md hover:bg-primary-foreground/10 cursor-pointer">
                  <div className="w-7 h-7 rounded-full bg-secondary/20 border-2 border-secondary/40 text-secondary flex items-center justify-center text-xs font-bold">
                    {user.avatar}
                  </div>
                  <div className="hidden md:flex flex-col leading-tight text-primary-foreground">
                    <span className="text-xs font-semibold truncate max-w-[100px]">
                      {user.name.split(" ")[0]}
                    </span>
                    <span className="text-[10px] text-primary-foreground/50">{user.id.slice(0, 10)}</span>
                  </div>
                </div>

                {/* Panier */}
                <button
                  onClick={() => setShowHistory(true)}
                  className="relative p-2 rounded-md hover:bg-primary-foreground/10 transition-colors text-primary-foreground"
                >
                  <ShoppingBag className="w-5 h-5" />
                  <span className="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] bg-secondary text-secondary-foreground text-[10px] font-bold rounded-full flex items-center justify-center">
                    {user.orders?.reduce((acc, o) => acc + (o.quantity || 1), 0) || 0}
                  </span>
                </button>

                {/* Logout */}
                <button
                  onClick={clearUser}
                  className="p-2 rounded-md hover:bg-primary-foreground/10 transition-colors text-primary-foreground/50 hover:text-primary-foreground"
                  title="Changer d'utilisateur"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowLogin(true)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-md border border-secondary/60 text-secondary hover:bg-secondary hover:text-secondary-foreground transition-all text-sm font-medium"
              >
                <UserIcon className="w-4 h-4" />
                <span className="hidden sm:inline">Se connecter</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* User context bar */}
      {isConnected && user && (
        <section className="bg-card border-b border-border">
          <div className="max-w-[1400px] mx-auto px-4 py-3 flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-secondary text-secondary-foreground flex items-center justify-center font-bold text-sm shrink-0">
              {user.avatar}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="font-bold text-sm text-card-foreground">{user.name}</h2>
                <span className="text-[11px] font-mono text-muted-foreground bg-muted px-1.5 py-0.5 rounded">
                  {user.id}
                </span>
              </div>
              <p className="text-[11px] text-muted-foreground mt-0.5">
                {user.orders?.reduce((acc, o) => acc + (o.quantity || 1), 0) || 0} articles achetés
              </p>
            </div>
            <div className="hidden md:flex items-center gap-2 px-3 py-2 rounded-lg bg-muted text-xs">
              <span className="text-secondary">{MODEL_ICONS[model]}</span>
              <span className="font-medium text-card-foreground">{MODEL_LABELS[model].name}</span>
            </div>
          </div>
        </section>
      )}

      {/* Product grid */}
      <main className="flex-1 max-w-[1400px] mx-auto px-4 py-6 w-full">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-bold text-base text-foreground">
            {isSearchMode
              ? `Resultats pour "${searchQuery}" (${displayProducts.length})`
              : isConnected && model !== "popular"
                ? `Recommandations pour ${user?.name}`
                : "Produits les plus populaires"}
          </h2>
          {isSearchMode ? (
            <button
              onClick={clearSearch}
              className="text-xs bg-secondary/10 text-secondary px-2.5 py-1 rounded-full font-medium hover:bg-secondary/20"
            >
              Effacer la recherche
            </button>
          ) : model !== "popular" && !isConnected && (
            <span className="text-xs bg-secondary/10 text-secondary px-2.5 py-1 rounded-full font-medium">
              Connectez-vous pour activer ce modèle
            </span>
          )}
        </div>

        {/* Erreur de recommandation (banner) */}
        {recommendationError && (
          <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-4 mb-4 flex items-center gap-3">
            <span className="text-amber-600 text-lg">!</span>
            <p className="text-sm text-amber-700">{recommendationError}</p>
          </div>
        )}

        {/* Grille de produits */}
        {displayProducts.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {displayProducts.map((product, i) => (
              <ProductCard
                key={product.id}
                product={product}
                rank={i + 1}
                onClick={fetchSimilarProducts}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-muted-foreground">
            Chargement...
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-primary text-primary-foreground/60 mt-auto">
        <div className="max-w-[1400px] mx-auto px-4 py-6 text-center text-xs">
          <p className="text-primary-foreground/50">RecoShop © 2026 - DATA & AI course</p>
        </div>
      </footer>

      {/* Modals */}
      {showHistory && isConnected && user && (
        <OrderHistory
          user={user}
          orders={user.orders || []}
          onClose={() => setShowHistory(false)}
        />
      )}
      {showLogin && <LoginDialog onClose={() => setShowLogin(false)} />}
      {selectedProduct && (
        <SimilarProductsModal
          product={selectedProduct}
          similarProducts={similarProducts}
          onClose={closeSimilarProducts}
        />
      )}
    </div>
  )
}
