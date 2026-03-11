# CLAUDE.md

## General Rules

- **Never commit** on my behalf. Always ask before running any git commit.
- **Think before editing.** Analyze the problem, outline your approach, and ask for clarification on ambiguous situations before making any changes.
- Do not write comments in the code.
- Always use the `.env.example` file as reference for environment variables and API keys.

## Project Overview

A chat application that helps users find places to go out in the city. An AI agent (powered by Claude API) converses with the user, checks tomorrow's weather, scrapes the web for venue suggestions based on the user's query, and recommends where to go and what to wear.

### Core Features

1. **Chat interface** — User interacts via a conversational API
2. **Weather forecast** — Fetches tomorrow's weather from Open-Meteo (free, no API key)
3. **Place discovery** — Scrapes the web for venues (restaurants, bars, cafes, events) matching the user's query. No paid APIs, use simple HTTP scraping (e.g., BeautifulSoup + requests)
4. **AI recommendations** — Claude agent synthesizes weather + places + user preferences to suggest where to go and what to wear
5. **User data** — All user info, preferences, and chat history stored in a single JSON file

## Tech Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **AI:** Anthropic SDK (Claude API)
- **Weather:** Open-Meteo API (free, no key required)
- **Scraping:** requests + BeautifulSoup4
- **Data storage:** Single JSON file (no database)
- **Environment:** virtualenv + requirements.txt

## Architecture — Clean Architecture

### Layer 1: Domain (Entities)

Core business objects with no external dependencies.

- `User` — id, name, city, preferences
- `ChatMessage` — role, content, timestamp
- `ChatSession` — user_id, messages list
- `WeatherForecast` — date, temperature, conditions, humidity, wind
- `Place` — name, type, location, description, rating, url
- `Recommendation` — places list, outfit suggestion, reasoning

### Layer 2: Use Cases (Application Services)

Business logic orchestration. Depends only on domain entities and port interfaces.

- `ChatUseCase` — Manages conversation flow, delegates to agent
- `WeatherUseCase` — Retrieves and processes tomorrow's forecast
- `PlaceSearchUseCase` — Triggers web scraping for venues
- `RecommendationUseCase` — Combines weather + places + preferences into a suggestion
- `UserUseCase` — CRUD operations on user data

### Layer 3: Interfaces (Adapters)

Ports and adapters that connect use cases to the outside world.

**Ports (abstract interfaces):**
- `WeatherPort` — abstract interface for weather data retrieval
- `ScraperPort` — abstract interface for web scraping
- `AIAgentPort` — abstract interface for LLM interaction
- `StoragePort` — abstract interface for data persistence

**Adapters (API layer):**
- FastAPI routers exposing HTTP endpoints

### Layer 4: Infrastructure (External Services)

Concrete implementations of ports.

- `OpenMeteoClient` — implements `WeatherPort`, calls Open-Meteo API
- `WebScraper` — implements `ScraperPort`, uses requests + BeautifulSoup
- `ClaudeAgent` — implements `AIAgentPort`, uses Anthropic SDK
- `JsonFileStorage` — implements `StoragePort`, reads/writes the single JSON file

### Dependency Injection

Use dependency injection to wire infrastructure implementations to use case ports. FastAPI's `Depends()` system handles injection at the router level. A central `container` module creates and provides all dependencies.

## Project Structure

```
ubiquitous-telegram/
├── CLAUDE.md
├── .env.example
├── requirements.txt
├── app/
│   ├── main.py                     # FastAPI app entry point
│   ├── config.py                   # Loads env vars via pydantic Settings
│   ├── container.py                # Dependency injection wiring
│   ├── domain/
│   │   ├── entities.py             # User, ChatMessage, ChatSession, WeatherForecast, Place, Recommendation
│   │   └── ports.py                # WeatherPort, ScraperPort, AIAgentPort, StoragePort
│   ├── use_cases/
│   │   ├── chat.py                 # ChatUseCase
│   │   ├── weather.py              # WeatherUseCase
│   │   ├── place_search.py         # PlaceSearchUseCase
│   │   ├── recommendation.py       # RecommendationUseCase
│   │   └── user.py                 # UserUseCase
│   ├── adapters/
│   │   └── api/
│   │       ├── routes_chat.py      # Chat endpoints
│   │       ├── routes_user.py      # User endpoints
│   │       └── schemas.py          # Pydantic request/response models
│   └── infrastructure/
│       ├── weather_client.py       # OpenMeteoClient
│       ├── web_scraper.py          # WebScraper (BeautifulSoup)
│       ├── claude_agent.py         # ClaudeAgent (Anthropic SDK)
│       └── json_storage.py         # JsonFileStorage
└── data/
    └── app_data.json               # Single JSON file for all data
```

## Data File Structure (app_data.json)

```json
{
  "users": {
    "user_id": {
      "id": "user_id",
      "name": "string",
      "city": "string",
      "preferences": {}
    }
  },
  "sessions": {
    "session_id": {
      "user_id": "user_id",
      "messages": [
        {
          "role": "user|assistant",
          "content": "string",
          "timestamp": "ISO8601"
        }
      ]
    }
  }
}
```

## Environment Variables

Reference `.env.example` for all required variables:

- `CLAUDE_API_KEY` — Anthropic API key for Claude
- `OPEN_METEO_BASE_URL` — Base URL for Open-Meteo API
- `APP_HOST` — Application host
- `APP_PORT` — Application port
- `DATA_DIR` — Directory for the JSON data file

## API Endpoints

### Users — `/api/users`

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|-------------|----------|
| `POST` | `/api/users` | Create a new user | `{ name, city, preferences }` | `201` — created user |
| `GET` | `/api/users/{user_id}` | Get user by ID | — | `200` — user object |
| `PUT` | `/api/users/{user_id}` | Update user profile | `{ name?, city?, preferences? }` | `200` — updated user |
| `DELETE` | `/api/users/{user_id}` | Delete user and all their sessions | — | `204` — no content |

### Chat — `/api/chat`

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|-------------|----------|
| `POST` | `/api/chat/sessions` | Start a new chat session for a user | `{ user_id }` | `201` — session with id |
| `GET` | `/api/chat/sessions/{session_id}` | Get full chat history for a session | — | `200` — session with messages |
| `POST` | `/api/chat/sessions/{session_id}/messages` | Send a message and get AI response | `{ content }` | `200` — assistant message with recommendation |
| `DELETE` | `/api/chat/sessions/{session_id}` | Delete a chat session | — | `204` — no content |
| `GET` | `/api/chat/users/{user_id}/sessions` | List all sessions for a user | — | `200` — list of session summaries |

### Weather — `/api/weather`

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|-------------|----------|
| `GET` | `/api/weather/{city}` | Get tomorrow's weather forecast for a city | — | `200` — forecast object (temperature, conditions, humidity, wind) |

### Places — `/api/places`

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|-------------|----------|
| `GET` | `/api/places/search` | Search for places in a city | Query params: `city`, `query`, `type?` | `200` — list of places |

### Health — `/api`

| Method | Path | Description | Response |
|--------|------|-------------|----------|
| `GET` | `/api/health` | Health check | `200` — `{ status: "ok" }` |

### Notes

- The main endpoint is `POST /api/chat/sessions/{session_id}/messages` — this is where the AI agent orchestrates everything: it reads the user message, fetches weather, scrapes places if needed, and returns a recommendation.
- Weather and Places endpoints are also exposed standalone so the frontend or debugging tools can call them independently.
- All endpoints return JSON. Errors return `{ detail: "error message" }` with appropriate HTTP status codes (400, 404, 422, 500).

## Error Handling

- Handle all errors explicitly with FastAPI exception handlers
- Use proper HTTP status codes
- Never let unhandled exceptions reach the client
- Validate all input with Pydantic models

## Setup

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in values
5. Run: `uvicorn app.main:app --host $APP_HOST --port $APP_PORT`
