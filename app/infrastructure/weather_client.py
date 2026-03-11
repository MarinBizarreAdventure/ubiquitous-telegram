from datetime import date, timedelta

import requests

from app.domain.entities import WeatherForecast
from app.domain.ports import WeatherPort


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

WMO_CONDITIONS = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


class OpenMeteoClient(WeatherPort):
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    def _get_coordinates(self, city: str) -> tuple[float, float]:
        response = requests.get(GEOCODING_URL, params={"name": city, "count": 1}, timeout=10)
        response.raise_for_status()
        results = response.json().get("results")
        if not results:
            raise ValueError(f"City '{city}' not found")
        return results[0]["latitude"], results[0]["longitude"]

    def get_tomorrow_forecast(self, city: str) -> WeatherForecast:
        lat, lon = self._get_coordinates(city)
        tomorrow = (date.today() + timedelta(days=1)).isoformat()

        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum,windspeed_10m_max,relativehumidity_2m_max",
            "timezone": "auto",
            "start_date": tomorrow,
            "end_date": tomorrow,
        }
        response = requests.get(f"{self._base_url}/v1/forecast", params=params, timeout=10)
        response.raise_for_status()
        daily = response.json()["daily"]

        wmo_code = daily["weathercode"][0]
        conditions = WMO_CONDITIONS.get(wmo_code, f"Weather code {wmo_code}")

        return WeatherForecast(
            date=tomorrow,
            temperature_min=daily["temperature_2m_min"][0],
            temperature_max=daily["temperature_2m_max"][0],
            conditions=conditions,
            humidity=daily["relativehumidity_2m_max"][0],
            wind_speed=daily["windspeed_10m_max"][0],
        )
