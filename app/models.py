from dataclasses import dataclass, field
from pydantic import BaseModel


@dataclass
class User:
    id: str
    name: str
    city: str
    preferences: dict = field(default_factory=dict)


class CreateUserRequest(BaseModel):
    name: str
    city: str
    preferences: dict = {}


class UserResponse(BaseModel):
    id: str
    name: str
    city: str
    preferences: dict


class AgentRequest(BaseModel):
    user_id: str
    message: str


class AgentResponse(BaseModel):
    reply: str
