from app.domain.entities import WeatherForecast
from app.domain.ports import WeatherPort


class WeatherUseCase:
    def __init__(self, weather: WeatherPort) -> None:
        self._weather = weather

    def get_tomorrow_forecast(self, city: str) -> WeatherForecast:
        return self._weather.get_tomorrow_forecast(city)
