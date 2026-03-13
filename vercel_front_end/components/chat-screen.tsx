'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { LogOut, MapPin, Send } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ThemeToggle } from './theme-toggle'
import { ChatMessage } from './chat-message'
import { TypingIndicator } from './typing-indicator'
import type { Message, User } from '@/lib/types'

interface ChatScreenProps {
  user: User
  onLogout: () => void
}

export function ChatScreen({ user, onLogout }: ChatScreenProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading, scrollToBottom])

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: messageText.trim(),
      places: [],
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.id,
          message: messageText.trim(),
        }),
        signal: AbortSignal.timeout(60000),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Failed to get response')
      }

      const data = await response.json()
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.reply,
        places: data.places || [],
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      const errorMessage: Message = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${err instanceof Error ? err.message : 'Something went wrong'}. Please try again.`,
        places: [],
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  const handleAskMore = (placeName: string) => {
    const prefilled = `Tell me more about ${placeName}`
    setInput(prefilled)
    inputRef.current?.focus()
  }

  return (
    <div className="flex h-screen flex-col bg-background">
      {/* Header */}
      <header className="flex items-center justify-between border-b px-4 py-3">
        <div className="flex items-center gap-2">
          <MapPin className="h-5 w-5 text-primary" />
          <span className="font-semibold">City Guide</span>
        </div>
        <div className="flex items-center gap-1 text-sm text-muted-foreground">
          <span className="font-medium text-foreground">{user.name}</span>
          <span>•</span>
          <span>{user.city}</span>
        </div>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Button variant="ghost" size="sm" onClick={onLogout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </header>

      {/* Messages area */}
      <main className="flex-1 overflow-y-auto p-4">
        <div className="mx-auto max-w-3xl space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <MapPin className="h-8 w-8 text-primary" />
              </div>
              <h2 className="mb-2 text-xl font-semibold">Welcome, {user.name}!</h2>
              <p className="max-w-md text-muted-foreground">
                Ask me about places to visit in {user.city}. I can recommend restaurants, bars, 
                activities, and even tell you what to wear based on tomorrow&apos;s weather!
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <ChatMessage
              key={index}
              message={message}
              onAskMore={handleAskMore}
            />
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="rounded-2xl bg-muted">
                <TypingIndicator />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input area */}
      <footer className="border-t p-4">
        <form onSubmit={handleSubmit} className="mx-auto flex max-w-3xl gap-2">
          <Input
            ref={inputRef}
            type="text"
            placeholder="Ask about places to visit..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={isLoading || !input.trim()}>
            <Send className="h-4 w-4" />
            <span className="sr-only">Send message</span>
          </Button>
        </form>
      </footer>
    </div>
  )
}
