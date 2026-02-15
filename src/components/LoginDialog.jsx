import { useState } from "react"
import { X, Shuffle, Search } from "lucide-react"
import useGlobalStore from "../stores/useGlobalStore"

export default function LoginDialog({ onClose }) {
  const [mode, setMode] = useState("choose")
  const [userId, setUserId] = useState("")

  const { generateRandomUser, loadUserById } = useGlobalStore()

  const handleRandomUser = () => {
    generateRandomUser()
    onClose()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (userId.trim()) {
      loadUserById(userId.trim())
      onClose()
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-card rounded-xl shadow-2xl w-full max-w-sm mx-4 p-6 animate-in zoom-in-95 duration-200">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-muted-foreground hover:text-foreground"
        >
          <X className="w-5 h-5" />
        </button>

        <h2 className="text-xl font-bold text-card-foreground mb-6">
          Sélectionner un utilisateur
        </h2>

        {mode === "choose" ? (
          <div className="space-y-3">
            <button
              onClick={handleRandomUser}
              className="w-full flex items-center gap-3 p-4 rounded-lg border border-border hover:bg-muted transition-colors"
            >
              <div className="w-10 h-10 rounded-full bg-secondary/20 flex items-center justify-center">
                <Shuffle className="w-5 h-5 text-secondary" />
              </div>
              <div className="text-left">
                <p className="font-semibold text-card-foreground">Utilisateur aléatoire</p>
                <p className="text-xs text-muted-foreground">Sélectionner un ID au hasard</p>
              </div>
            </button>

            <button
              onClick={() => setMode("enter-id")}
              className="w-full flex items-center gap-3 p-4 rounded-lg border border-border hover:bg-muted transition-colors"
            >
              <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                <Search className="w-5 h-5 text-primary" />
              </div>
              <div className="text-left">
                <p className="font-semibold text-card-foreground">Entrer un ID</p>
                <p className="text-xs text-muted-foreground">Charger un utilisateur spécifique</p>
              </div>
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-card-foreground mb-2">
                ID Utilisateur
              </label>
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Ex: A2SUAM1J3GNN3B"
                autoFocus
                className="w-full px-4 py-2 rounded-lg border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setMode("choose")}
                className="flex-1 px-4 py-2 rounded-lg border border-border text-card-foreground hover:bg-muted transition-colors"
              >
                Retour
              </button>
              <button
                type="submit"
                disabled={!userId.trim()}
                className="flex-1 px-4 py-2 rounded-lg bg-primary text-primary-foreground font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
              >
                Charger
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
