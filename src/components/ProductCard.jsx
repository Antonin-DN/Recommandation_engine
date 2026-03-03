import { useState } from "react"
import { Star, Sparkles, Info, X } from "lucide-react"

export default function ProductCard({ product, rank, onClick }) {
  const [showInfo, setShowInfo] = useState(false)
  const hasEmbedding = !!product.description

  return (
    <div
      className={`group bg-card rounded-lg overflow-hidden card-hover relative ${hasEmbedding ? "cursor-pointer" : ""}`}
      onClick={hasEmbedding ? () => onClick?.(product) : undefined}
    >
      {/* Badge de classement */}
      {rank && (
        <div className={`absolute top-2 left-2 z-10 px-2 py-0.5 rounded text-xs font-bold ${
          rank <= 3
            ? "bg-secondary text-secondary-foreground"
            : "bg-muted text-muted-foreground"
        }`}>
          {rank <= 3 ? `#${rank} Best Seller` : `#${rank}`}
        </div>
      )}

      {/* Badge RAG */}
      {hasEmbedding && (
        <div className="absolute top-2 right-2 z-10 p-1.5 rounded-full bg-primary/90 text-secondary" title="Voir produits similaires">
          <Sparkles className="w-3 h-3" />
        </div>
      )}

      {/* Bouton Info (hors panel) */}
      {!showInfo && (
        <button
          onClick={(e) => { e.stopPropagation(); setShowInfo(true) }}
          className="absolute bottom-2 right-2 z-10 p-1.5 rounded-full bg-muted/90 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
          title="Voir les details"
        >
          <Info className="w-3 h-3" />
        </button>
      )}

      {/* Panel Info */}
      {showInfo && (
        <div
          className="absolute inset-0 z-20 bg-card p-3 overflow-auto flex flex-col"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Bouton fermer */}
          <button
            onClick={(e) => { e.stopPropagation(); setShowInfo(false) }}
            className="absolute top-2 right-2 p-1.5 rounded-full bg-muted text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-3 h-3" />
          </button>

          <p className="text-[9px] font-mono text-muted-foreground mb-2 break-all pr-8">
            {product.id}
          </p>
          {product.category && (
            <span className="text-[10px] bg-secondary/20 text-secondary px-1.5 py-0.5 rounded w-fit mb-2">
              {product.category}
            </span>
          )}
          <p className="text-xs font-semibold text-card-foreground mb-2 line-clamp-3">
            {product.name}
          </p>
          {product.description && (
            <p className="text-[11px] text-muted-foreground flex-1 overflow-auto">
              {product.description}
            </p>
          )}
          {(product.score || product.similarity) && (
            <div className="mt-2 pt-2 border-t border-border">
              <p className="text-[10px] text-muted-foreground">
                {product.similarity
                  ? `Similarite: ${Math.round(product.similarity * 100)}%`
                  : `Score: ${product.score?.toFixed(2)}`
                }
              </p>
            </div>
          )}
        </div>
      )}

      {/* Image */}
      <div className="aspect-[4/3] overflow-hidden bg-muted">
        <img
          src={product.image}
          alt={product.name}
          loading="lazy"
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
      </div>

      {/* Contenu */}
      <div className="p-3">
        {product.category && (
          <p className="text-[10px] uppercase tracking-wider text-secondary mb-1">
            {product.category}
          </p>
        )}
        <h3 className="font-semibold text-sm text-card-foreground line-clamp-2 mb-2">
          {product.name}
        </h3>

        {/* Rating */}
        <div className="flex items-center gap-1 mb-2">
          <div className="flex">
            {[1, 2, 3, 4, 5].map((i) => (
              <Star
                key={i}
                className={`w-3 h-3 ${
                  i <= Math.round(product.rating)
                    ? "fill-star text-star"
                    : "text-muted"
                }`}
              />
            ))}
          </div>
          <span className="text-xs text-muted-foreground">
            ({product.reviewCount})
          </span>
        </div>

        {/* Prix */}
        <p className="font-bold text-base text-card-foreground">
          {product.price.toFixed(2)} €
        </p>
      </div>
    </div>
  )
}
