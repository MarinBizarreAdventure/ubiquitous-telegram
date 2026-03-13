export function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 px-3 py-2">
      <span className="sr-only">Assistant is typing</span>
      <div className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/60 [animation-delay:-0.3s]" />
      <div className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/60 [animation-delay:-0.15s]" />
      <div className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/60" />
    </div>
  )
}
