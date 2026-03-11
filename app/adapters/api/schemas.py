from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    city: str
    preferences: dict = {}


class UpdateUserRequest(BaseModel):
    name: str | None = None
    city: str | None = None
    preferences: dict | None = None


class UserResponse(BaseModel):
    id: str
    name: str
    city: str
    preferences: dict


class CreateSessionRequest(BaseModel):
    user_id: str


class ChatMessageResponse(BaseModel):
    role: str
    content: str
    timestamp: str


class SessionResponse(BaseModel):
    id: str
    user_id: str
    messages: list[ChatMessageResponse]


class SessionSummaryResponse(BaseModel):
    id: str
    user_id: str
    message_count: int


class SendMessageRequest(BaseModel):
    content: str


class WeatherResponse(BaseModel):
    date: str
    temperature_min: float
    temperature_max: float
    conditions: str
    humidity: float
    wind_speed: float


class PlaceResponse(BaseModel):
    name: str
    type: str
    location: str
    description: str
    url: str
    rating: str


class HealthResponse(BaseModel):
    status: str
