'use client'

import { useEffect, useState } from 'react'
import { OnboardingScreen } from '@/components/onboarding-screen'
import { ChatScreen } from '@/components/chat-screen'
import type { User } from '@/lib/types'

export default function Home() {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const stored = localStorage.getItem('cityguide_user')
    if (stored) {
      try {
        setUser(JSON.parse(stored))
      } catch {
        localStorage.removeItem('cityguide_user')
      }
    }
    setIsLoading(false)
  }, [])

  const handleUserCreated = (newUser: User) => {
    setUser(newUser)
  }

  const handleLogout = () => {
    localStorage.removeItem('cityguide_user')
    setUser(null)
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    )
  }

  if (!user) {
    return <OnboardingScreen onUserCreated={handleUserCreated} />
  }

  return <ChatScreen user={user} onLogout={handleLogout} />
}
