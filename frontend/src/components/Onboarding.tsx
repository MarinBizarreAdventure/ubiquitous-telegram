import { useState } from "react"
import { createUser } from "../api"
import type { User } from "../types"

interface Props {
  onDone: (user: User) => void
}

export default function Onboarding({ onDone }: Props) {
  const [name, setName] = useState("")
  const [city, setCity] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!name.trim() || !city.trim()) return
    setLoading(true)
    setError("")
    try {
      const user = await createUser(name.trim(), city.trim())
      onDone(user)
    } catch {
      setError("Could not connect to server. Make sure the backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="onboarding">
      <div className="onboarding-card">
        <h1>🌆 City Guide</h1>
        <p>Tell me who you are and I'll help you find the perfect place to go out.</p>
        <form onSubmit={handleSubmit}>
          <label>
            Your name
            <input
              type="text"
              placeholder="e.g. Marin"
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoFocus
            />
          </label>
          <label>
            Your city
            <input
              type="text"
              placeholder="e.g. Chisinau"
              value={city}
              onChange={(e) => setCity(e.target.value)}
            />
          </label>
          {error && <p className="error">{error}</p>}
          <button type="submit" disabled={loading || !name.trim() || !city.trim()}>
            {loading ? "Setting up..." : "Start chatting →"}
          </button>
        </form>
      </div>
    </div>
  )
}
