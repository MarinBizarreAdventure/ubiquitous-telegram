from app.domain.entities import Place, Recommendation, WeatherForecast
from app.domain.ports import AIAgentPort


class RecommendationUseCase:
    def __init__(self, agent: AIAgentPort) -> None:
        self._agent = agent

    def get_recommendation(
        self,
        user_message: str,
        weather: WeatherForecast,
        places: list[Place],
        history: list[dict],
    ) -> Recommendation:
        return self._agent.get_recommendation(user_message, weather, places, history)
