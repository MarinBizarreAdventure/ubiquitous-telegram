from abc import ABC, abstractmethod

from app.domain.entities import ChatSession, Place, Recommendation, User, WeatherForecast


class StoragePort(ABC):
    @abstractmethod
    def get_user(self, user_id: str) -> User | None:
        ...

    @abstractmethod
    def save_user(self, user: User) -> User:
        ...

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        ...

    @abstractmethod
    def get_session(self, session_id: str) -> ChatSession | None:
        ...

    @abstractmethod
    def save_session(self, session: ChatSession) -> ChatSession:
        ...

    @abstractmethod
    def delete_session(self, session_id: str) -> None:
        ...

    @abstractmethod
    def get_sessions_by_user(self, user_id: str) -> list[ChatSession]:
        ...


class WeatherPort(ABC):
    @abstractmethod
    def get_tomorrow_forecast(self, city: str) -> WeatherForecast:
        ...


class ScraperPort(ABC):
    @abstractmethod
    def search_places(self, city: str, query: str, place_type: str | None = None) -> list[Place]:
        ...


class AIAgentPort(ABC):
    @abstractmethod
    def get_recommendation(
        self,
        user_message: str,
        weather: WeatherForecast,
        places: list[Place],
        history: list[dict],
    ) -> Recommendation:
        ...
