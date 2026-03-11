from functools import lru_cache

from app.config import settings
from app.infrastructure.claude_agent import ClaudeAgent
from app.infrastructure.json_storage import JsonFileStorage
from app.infrastructure.weather_client import OpenMeteoClient
from app.infrastructure.web_scraper import WebScraper
from app.use_cases.chat import ChatUseCase
from app.use_cases.place_search import PlaceSearchUseCase
from app.use_cases.user import UserUseCase
from app.use_cases.weather import WeatherUseCase


@lru_cache
def get_storage() -> JsonFileStorage:
    return JsonFileStorage(settings.data_dir)


@lru_cache
def get_weather_client() -> OpenMeteoClient:
    return OpenMeteoClient(settings.open_meteo_base_url)


@lru_cache
def get_scraper() -> WebScraper:
    return WebScraper()


@lru_cache
def get_agent() -> ClaudeAgent:
    return ClaudeAgent(settings.claude_api_key)


def get_user_use_case() -> UserUseCase:
    return UserUseCase(get_storage())


def get_weather_use_case() -> WeatherUseCase:
    return WeatherUseCase(get_weather_client())


def get_place_search_use_case() -> PlaceSearchUseCase:
    return PlaceSearchUseCase(get_scraper())


def get_chat_use_case() -> ChatUseCase:
    return ChatUseCase(
        storage=get_storage(),
        weather=get_weather_client(),
        scraper=get_scraper(),
        agent=get_agent(),
    )
