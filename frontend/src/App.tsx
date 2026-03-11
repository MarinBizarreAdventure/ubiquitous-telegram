import { useState } from "react"
import "./index.css"
import Chat from "./components/Chat"
import Onboarding from "./components/Onboarding"
import type { User } from "./types"

export default function App() {
  const [user, setUser] = useState<User | null>(null)

  if (!user) return <Onboarding onDone={setUser} />
  return <Chat user={user} />
}
