import { X, Star } from "lucide-react"

export default function OrderHistory({ user, orders, onClose }) {
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
              Historique des achats
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
          {orders.map((order, i) => (
            <div
              key={i}
              className="flex gap-3 p-3 rounded-lg bg-muted/50 border border-border"
            >
              <div className="w-12 h-12 rounded-lg bg-secondary/20 flex items-center justify-center text-secondary font-bold text-xs">
                {order.productName?.substring(0, 2).toUpperCase() || "??"}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm text-card-foreground line-clamp-2">
                  {order.productName || order.productId}
                </p>
                <p className="text-xs text-muted-foreground mt-0.5">
                  <span className="font-mono">{order.productId?.slice(0, 10)}</span> · {order.date}
                  {order.quantity > 1 && (
                    <span className="ml-2 px-1.5 py-0.5 bg-secondary/20 text-secondary rounded text-[10px] font-medium">
                      x{order.quantity}
                    </span>
                  )}
                </p>
                <div className="flex items-center gap-1 mt-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star
                      key={star}
                      className={`w-3 h-3 ${
                        star <= Math.round(order.rating)
                          ? "fill-star text-star"
                          : "text-muted"
                      }`}
                    />
                  ))}
                  <span className="text-xs text-muted-foreground ml-1">
                    {order.rating?.toFixed(1)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer summary */}
        <div className="p-4 border-t border-border bg-muted/30">
          <p className="text-sm text-muted-foreground">
            {orders.length} produit{orders.length > 1 ? "s" : ""} · {orders.reduce((acc, o) => acc + (o.quantity || 1), 0)} article{orders.reduce((acc, o) => acc + (o.quantity || 1), 0) > 1 ? "s" : ""}
          </p>
        </div>
      </div>
    </div>
  )
}
