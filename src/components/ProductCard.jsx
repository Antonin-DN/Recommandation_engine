import { Star } from "lucide-react"

export default function ProductCard({ product, rank }) {
  return (
    <div className="group bg-card rounded-lg overflow-hidden card-hover relative">
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
        <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-1">
          {product.category}
        </p>
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
