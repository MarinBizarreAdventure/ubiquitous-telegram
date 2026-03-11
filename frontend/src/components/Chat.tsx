import { useEffect, useRef, useState } from "react"
import { sendMessage } from "../api"
import type { Message, Place, User } from "../types"
import MessageBubble from "./MessageBubble"

interface Props {
  user: User
}

export default function Chat({ user }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: `Hey ${user.name}! 👋 Tell me what you feel like doing in ${user.city} tomorrow and I'll check the weather and find the best spots for you.`,
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  async function handleSend(e: React.FormEvent) {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading) return

    setMessages((prev) => [...prev, { role: "user", content: text }])
    setInput("")
    setLoading(true)

    try {
      const { reply, places } = await sendMessage(user.id, text)
      setMessages((prev) => [...prev, { role: "assistant", content: reply, places }])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, something went wrong. Please try again." },
      ])
    } finally {
      setLoading(false)
    }
  }

  function handleSelectPlace(place: Place) {
    setInput((prev) =>
      prev ? `${prev} Tell me more about "${place.name}".` : `Tell me more about "${place.name}".`
    )
  }

  return (
    <div className="chat">
      <header className="chat-header">
        <span className="chat-header-title">🌆 City Guide</span>
        <span className="chat-header-user">
          {user.name} · {user.city}
        </span>
      </header>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} onSelectPlace={handleSelectPlace} />
        ))}
        {loading && (
          <div className="message-row message-row--assistant">
            <div className="bubble bubble--assistant bubble--typing">
              <span />
              <span />
              <span />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="chat-input-area" onSubmit={handleSend}>
        <input
          type="text"
          placeholder="What do you want to do tomorrow?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          autoFocus
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}
