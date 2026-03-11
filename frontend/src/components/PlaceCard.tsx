import type { Place } from "../types"

interface Props {
  place: Place
  onSelect: (place: Place) => void
}

function imageUrl(place: Place): string {
  if (place.image_url) return place.image_url
  const keyword = encodeURIComponent(place.name.split(" ").slice(0, 2).join(","))
  const seed = place.name.split("").reduce((acc, c) => acc + c.charCodeAt(0), 0)
  return `https://loremflickr.com/480/280/${keyword}?lock=${seed}`
}

export default function PlaceCard({ place, onSelect }: Props) {
  const url = place.url.startsWith("http") ? place.url : `https://${place.url}`

  return (
    <div className="place-card">
      <div className="place-card-image">
        <img
          src={imageUrl(place)}
          alt={place.name}
          onError={(e) => {
            const target = e.target as HTMLImageElement
            target.src = `https://loremflickr.com/480/280/city,venue?lock=${place.name.length}`
          }}
        />
      </div>
      <div className="place-card-body">
        <h4>{place.name}</h4>
        <p>{place.description.slice(0, 100)}{place.description.length > 100 ? "…" : ""}</p>
        <div className="place-card-actions">
          <a href={url} target="_blank" rel="noreferrer" className="btn-link">
            Visit site ↗
          </a>
          <button className="btn-select" onClick={() => onSelect(place)}>
            Ask about this
          </button>
        </div>
      </div>
    </div>
  )
}
