'use client'

import { ExternalLink, MessageCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import type { Place } from '@/lib/types'

interface PlaceCardProps {
  place: Place
  onAskMore: (placeName: string) => void
}

export function PlaceCard({ place, onAskMore }: PlaceCardProps) {
  const imageUrl = place.image_url && place.image_url.trim() !== ''
    ? place.image_url
    : `https://loremflickr.com/400/250/${encodeURIComponent(place.name)}`

  return (
    <Card className="min-w-[280px] max-w-[320px] flex-shrink-0 overflow-hidden transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
      <div className="relative aspect-video w-full overflow-hidden">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={imageUrl}
          alt={place.name}
          className="h-full w-full object-cover"
          loading="lazy"
        />
      </div>
      <CardContent className="p-4">
        <div className="mb-2 flex items-start justify-between gap-2">
          <h4 className="line-clamp-1 font-semibold">{place.name}</h4>
          {place.url && (
            <a
              href={place.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-shrink-0 text-muted-foreground transition-colors hover:text-foreground"
              aria-label={`Open ${place.name} in new tab`}
            >
              <ExternalLink className="h-4 w-4" />
            </a>
          )}
        </div>
        <p className="mb-3 line-clamp-2 text-sm text-muted-foreground">
          {place.description || 'No description available'}
        </p>
        <Button
          variant="outline"
          size="sm"
          className="w-full"
          onClick={() => onAskMore(place.name)}
        >
          <MessageCircle className="mr-2 h-3 w-3" />
          Ask more
        </Button>
      </CardContent>
    </Card>
  )
}
