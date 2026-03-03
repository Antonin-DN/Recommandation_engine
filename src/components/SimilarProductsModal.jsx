import { X, Sparkles } from "lucide-react"
import ProductCard from "./ProductCard"

export default function SimilarProductsModal({ product, similarProducts, onClose }) {
  if (!product) return null

  return (
    <>
      {/* Overlay */}
      <div className="fixed inset-0 bg-black/60 z-50" onClick={onClose} />

      {/* Modal */}
      <div className="fixed inset-4 md:inset-8 bg-background rounded-xl z-50 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-4 border-b border-border flex items-start gap-4 bg-card">
          <img
            src={product.image}
            alt={product.name}
            className="w-16 h-16 rounded-lg object-cover"
          />
          <div className="flex-1 min-w-0">
            {product.category && (
              <p className="text-[10px] uppercase tracking-wider text-secondary mb-0.5">
                {product.category}
              </p>
            )}
            <h2 className="font-bold text-sm text-card-foreground line-clamp-2">
              {product.name}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-muted text-muted-foreground shrink-0"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Similar products */}
        <div className="flex-1 overflow-auto p-4">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-4 h-4 text-secondary" />
            <h3 className="font-semibold text-foreground">Vous pourriez aussi aimer</h3>
            <span className="text-xs text-muted-foreground ml-auto">
              Base sur la similarite semantique
            </span>
          </div>

          {similarProducts.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              Chargement...
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
              {similarProducts.map((p, i) => (
                <div key={p.id} className="relative">
                  <ProductCard product={p} />
                  {/* Badge similarité */}
                  <div className="absolute top-2 left-2 z-10 px-1.5 py-0.5 rounded text-[10px] font-bold bg-secondary text-secondary-foreground">
                    {Math.round(p.similarity * 100)}%
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  )
}
