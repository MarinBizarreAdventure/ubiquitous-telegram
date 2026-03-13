import logging
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")

from app.agent import run_agent
from app.config import settings
from app.models import AgentRequest, AgentResponse, CreateUserRequest, PlaceResult, User, UserResponse
from app.storage import create_storage

app = FastAPI(title="City Guide", version="1.0.0")
storage = create_storage(settings.database_url, settings.data_dir)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def unhandled(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/users", response_model=UserResponse, status_code=201)
def create_user(body: CreateUserRequest):
    user = User(
        id=str(uuid.uuid4()),
        name=body.name,
        city=body.city,
        preferences=body.preferences,
    )
    storage.save(user)
    return UserResponse(id=user.id, name=user.name, city=user.city, preferences=user.preferences)


@app.post("/api/agent", response_model=AgentResponse)
def agent(body: AgentRequest):
    user = storage.get(body.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found. Create a user first via POST /api/users.")

    reply, places = run_agent(
        user_name=user.name,
        user_city=user.city,
        message=body.message,
        api_key=settings.claude_api_key,
        open_meteo_base_url=settings.open_meteo_base_url,
    )
    return AgentResponse(
        reply=reply,
        places=[PlaceResult(**p) for p in places],
    )
