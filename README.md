# City Guide

AI-powered chat app that helps you find places to go out in the city. It checks tomorrow's weather, scrapes the web for venues, and recommends where to go and what to wear.

## Project Structure

```
ubiquitous-telegram/
├── app/                 # FastAPI backend
├── data/                # JSON data storage (local dev fallback)
├── vercel_front_end/    # Next.js frontend (Vercel v0)
├── frontend_claude/     # Next.js frontend (built with Claude)
├── docker-compose.yml   # Docker orchestration
├── Dockerfile.backend   # Backend container
├── .env.example         # Environment variables template
└── requirements.txt     # Python dependencies
```

## Quick Start with Docker (recommended)

The easiest way to run everything. Requires [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

### 1. Set your API key

```bash
cp .env.example .env
```

Edit `.env` and set `CLAUDE_API_KEY` to your Anthropic API key.

### 2. Start all services

**Linux / macOS:**
```bash
docker compose up --build
```

**Windows (PowerShell):**
```powershell
docker compose up --build
```

**Windows (CMD):**
```cmd
docker compose up --build
```

This starts 3 containers:
- **PostgreSQL** on port 5432
- **Backend** (FastAPI) on port 8000
- **Frontend** (Next.js) on port 3000

### 3. Open the app

Go to [http://localhost:3000](http://localhost:3000)

### Stop everything

```bash
docker compose down
```

To also delete the database volume:
```bash
docker compose down -v
```

### Rebuild after code changes

```bash
docker compose up --build
```

## Local Development (without Docker)

### 1. Backend (FastAPI)

```bash
# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your CLAUDE_API_KEY
# Leave DATABASE_URL empty to use JSON file storage

# Start the backend (runs on port 8000)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend (Next.js)

Two frontends are available — pick either one:

```bash
# Option A: Vercel frontend (port 3000)
cd vercel_front_end
npm install
npm run dev

# Option B: Claude frontend (port 3001)
cd frontend_claude
npm install
npm run dev -- -p 3001
```

Both proxy `/api/*` to `http://localhost:8000` via Next.js rewrites.

## Usage

1. Open the frontend in your browser
2. Enter your name and city on the onboarding screen
3. Chat with the AI agent about where to go
4. Click "Ask more" on place cards to follow up on specific venues
5. Toggle dark/light mode with the theme button in the header

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/users` | Create user `{ name, city, preferences }` |
| `POST` | `/api/agent` | Chat with AI agent `{ user_id, message }` |

### POST /api/users

```json
// Request
{ "name": "Marin", "city": "Chisinau", "preferences": {} }

// Response 201
{ "id": "uuid", "name": "Marin", "city": "Chisinau", "preferences": {} }
```

### POST /api/agent

```json
// Request
{ "user_id": "uuid-from-create-user", "message": "I want to play pool and eat pizza tomorrow night" }

// Response 200
{
  "reply": "Based on tomorrow's weather in Chisinau (12°C, overcast)...",
  "places": [
    {
      "name": "Billiard Hall",
      "url": "https://bookgame.io/en/club/13290/billiard-hall",
      "description": "Popular pool hall in central Chisinau",
      "image_url": ""
    }
  ]
}
```

The agent call takes 5-20 seconds as it runs Claude API calls + web scraping + weather fetching.

## Environment Variables

See `.env.example`:

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_API_KEY` | Anthropic API key (required) | — |
| `DATABASE_URL` | PostgreSQL connection string (Docker sets this automatically) | empty (uses JSON file) |
| `OPEN_METEO_BASE_URL` | Weather API base URL | `https://api.open-meteo.com` |
| `DATA_DIR` | Directory for JSON data file (only used without PostgreSQL) | `./data` |

## Storage

- **With Docker**: PostgreSQL (automatic, no config needed)
- **Without Docker**: JSON file in `data/app_data.json` (default when `DATABASE_URL` is not set)
- To use PostgreSQL without Docker, set `DATABASE_URL=postgresql://user:pass@localhost:5432/dbname` in `.env`
