from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: str
    name: str
    city: str
    preferences: dict = field(default_factory=dict)


@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ChatSession:
    id: str
    user_id: str
    messages: list[ChatMessage] = field(default_factory=list)


@dataclass
class WeatherForecast:
    date: str
    temperature_min: float
    temperature_max: float
    conditions: str
    humidity: float
    wind_speed: float


@dataclass
class Place:
    name: str
    type: str
    location: str
    description: str
    url: str = ""
    rating: str = ""


@dataclass
class Recommendation:
    places: list[Place]
    outfit_suggestion: str
    reasoning: str
