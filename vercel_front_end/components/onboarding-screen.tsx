'use client'

import { useState } from 'react'
import { MapPin, User as UserIcon, ArrowRight, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ThemeToggle } from './theme-toggle'
import type { User } from '@/lib/types'

interface OnboardingScreenProps {
  onUserCreated: (user: User) => void
}

export function OnboardingScreen({ onUserCreated }: OnboardingScreenProps) {
  const [name, setName] = useState('')
  const [city, setCity] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim() || !city.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name.trim(), city: city.trim(), preferences: {} }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Failed to create user')
      }

      const user: User = await response.json()
      localStorage.setItem('cityguide_user', JSON.stringify(user))
      onUserCreated(user)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="flex items-center justify-end p-4">
        <ThemeToggle />
      </header>
      <main className="flex flex-1 items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
              <MapPin className="h-8 w-8 text-primary" />
            </div>
            <CardTitle className="text-2xl font-bold">City Guide</CardTitle>
            <CardDescription className="text-base">
              Find the best places to hang out
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <div className="relative">
                  <UserIcon className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Your name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="pl-10"
                    disabled={isLoading}
                    required
                  />
                </div>
              </div>
              <div className="space-y-2">
                <div className="relative">
                  <MapPin className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Your city"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="pl-10"
                    disabled={isLoading}
                    required
                  />
                </div>
              </div>
              {error && (
                <p className="text-sm text-destructive">{error}</p>
              )}
              <Button
                type="submit"
                className="w-full"
                disabled={isLoading || !name.trim() || !city.trim()}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating profile...
                  </>
                ) : (
                  <>
                    Get Started
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
