import { X, Star } from "lucide-react"

export default function OrderHistory({ user, orders, products, onClose }) {
  const getProduct = (productId) => products.find((p) => p.id === productId)

  const totalAmount = orders.reduce((sum, order) => {
    const product = getProduct(order.productId)
    return sum + (product ? product.price * order.quantity : 0)
  }, 0)

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="relative w-full max-w-md bg-card h-full shadow-2xl animate-in slide-in-from-right duration-300 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-border flex items-center justify-between">
          <div>
            <h2 className="font-bold text-lg text-card-foreground">
              Historique des commandes
            </h2>
            <p className="text-sm text-muted-foreground">{user.name}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Orders list */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {orders.map((order, i) => {
            const product = getProduct(order.productId)
            if (!product) return null

            return (
              <div
                key={i}
                className="flex gap-3 p-3 rounded-lg bg-muted/50 border border-border"
              >
                <img
                  src={product.image}
                  alt={product.name}
                  className="w-16 h-16 rounded-lg object-cover"
                />
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm text-card-foreground line-clamp-1">
                    {product.name}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {order.date} · Qté: {order.quantity}
                  </p>
                  <div className="flex items-center gap-1 mt-1">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <Star
                        key={i}
                        className={`w-3 h-3 ${
                          i <= Math.round(order.rating)
                            ? "fill-star text-star"
                            : "text-muted"
                        }`}
                      />
                    ))}
                    <span className="text-xs text-muted-foreground ml-1">
                      {order.rating.toFixed(1)}
                    </span>
                  </div>
                </div>
                <p className="font-semibold text-sm text-card-foreground">
                  {(product.price * order.quantity).toFixed(2)} €
                </p>
              </div>
            )
          })}
        </div>

        {/* Footer summary */}
        <div className="p-4 border-t border-border bg-muted/30">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm text-muted-foreground">
                {orders.length} commande{orders.length > 1 ? "s" : ""}
              </p>
              <p className="font-bold text-lg text-card-foreground">
                Total: {totalAmount.toFixed(2)} €
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
