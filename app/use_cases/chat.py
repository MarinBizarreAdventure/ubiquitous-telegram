import uuid

from app.domain.entities import ChatMessage, ChatSession, User
from app.domain.ports import AIAgentPort, ScraperPort, StoragePort, WeatherPort
from app.use_cases.place_search import PlaceSearchUseCase
from app.use_cases.recommendation import RecommendationUseCase
from app.use_cases.weather import WeatherUseCase


class ChatUseCase:
    def __init__(
        self,
        storage: StoragePort,
        weather: WeatherPort,
        scraper: ScraperPort,
        agent: AIAgentPort,
    ) -> None:
        self._storage = storage
        self._weather_uc = WeatherUseCase(weather)
        self._places_uc = PlaceSearchUseCase(scraper)
        self._recommendation_uc = RecommendationUseCase(agent)

    def create_session(self, user_id: str) -> ChatSession:
        user = self._storage.get_user(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        session = ChatSession(id=str(uuid.uuid4()), user_id=user_id)
        return self._storage.save_session(session)

    def get_session(self, session_id: str) -> ChatSession:
        session = self._storage.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")
        return session

    def get_sessions_by_user(self, user_id: str) -> list[ChatSession]:
        return self._storage.get_sessions_by_user(user_id)

    def delete_session(self, session_id: str) -> None:
        self.get_session(session_id)
        self._storage.delete_session(session_id)

    def send_message(self, session_id: str, content: str) -> ChatMessage:
        session = self.get_session(session_id)
        user = self._storage.get_user(session.user_id)
        if user is None:
            raise ValueError(f"User {session.user_id} not found")

        user_message = ChatMessage(role="user", content=content)
        session.messages.append(user_message)

        weather = self._weather_uc.get_tomorrow_forecast(user.city)
        places = self._places_uc.search(user.city, content)
        history = [{"role": m.role, "content": m.content} for m in session.messages[:-1]]
        recommendation = self._recommendation_uc.get_recommendation(content, weather, places, history)

        response_content = self._format_response(recommendation)
        assistant_message = ChatMessage(role="assistant", content=response_content)
        session.messages.append(assistant_message)
        self._storage.save_session(session)

        return assistant_message

    def _format_response(self, recommendation) -> str:
        place_lines = "\n".join(
            f"- {p.name} ({p.type}): {p.description}" for p in recommendation.places
        )
        return (
            f"{recommendation.reasoning}\n\n"
            f"**Places to consider:**\n{place_lines}\n\n"
            f"**What to wear:** {recommendation.outfit_suggestion}"
        )
