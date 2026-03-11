import type { Message, Place } from "../types"
import PlaceCard from "./PlaceCard"

interface Props {
  message: Message
  onSelectPlace: (place: Place) => void
}

export default function MessageBubble({ message, onSelectPlace }: Props) {
  const isUser = message.role === "user"

  return (
    <div className={`message-row ${isUser ? "message-row--user" : "message-row--assistant"}`}>
      <div className={`bubble ${isUser ? "bubble--user" : "bubble--assistant"}`}>
        {message.content.split("\n").map((line, i) => (
          <p key={i}>{line}</p>
        ))}
      </div>
      {!isUser && message.places && message.places.length > 0 && (
        <div className="places-grid">
          {message.places.map((place) => (
            <PlaceCard key={place.name} place={place} onSelect={onSelectPlace} />
          ))}
        </div>
      )}
    </div>
  )
}
