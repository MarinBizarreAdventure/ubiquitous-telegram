'use client'

import ReactMarkdown from 'react-markdown'
import { PlaceCard } from './place-card'
import type { Message } from '@/lib/types'

interface ChatMessageProps {
  message: Message
  onAskMore: (placeName: string) => void
}

export function ChatMessage({ message, onAskMore }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex max-w-[85%] flex-col gap-3 ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`rounded-2xl px-4 py-3 ${
            isUser
              ? 'bg-blue-600 text-white dark:bg-indigo-600'
              : 'bg-muted text-foreground'
          }`}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none dark:prose-invert prose-headings:mb-2 prose-headings:mt-4 prose-headings:first:mt-0 prose-p:my-2 prose-ul:my-2 prose-li:my-0">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
        
        {!isUser && message.places && message.places.length > 0 && (
          <div className="w-full">
            <div className="flex gap-3 overflow-x-auto pb-2 sm:flex-row max-sm:flex-col max-sm:overflow-x-visible">
              {message.places.map((place, index) => (
                <PlaceCard key={`${place.name}-${index}`} place={place} onAskMore={onAskMore} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
