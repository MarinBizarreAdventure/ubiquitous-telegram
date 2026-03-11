import type { Place, User } from "./types"

const BASE = "http://localhost:8000"

export async function createUser(name: string, city: string): Promise<User> {
  const res = await fetch(`${BASE}/api/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, city, preferences: {} }),
  })
  if (!res.ok) throw new Error("Failed to create user")
  return res.json()
}

export async function sendMessage(
  userId: string,
  message: string
): Promise<{ reply: string; places: Place[] }> {
  const res = await fetch(`${BASE}/api/agent`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message }),
  })
  if (!res.ok) throw new Error("Agent request failed")
  return res.json()
}
