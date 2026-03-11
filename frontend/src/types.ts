export interface User {
  id: string
  name: string
  city: string
}

export interface Place {
  name: string
  url: string
  description: string
  image_url: string
}

export interface Message {
  role: "user" | "assistant"
  content: string
  places?: Place[]
}
