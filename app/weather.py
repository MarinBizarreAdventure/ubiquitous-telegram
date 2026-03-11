from datetime import date, timedelta

import requests

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


def get_tomorrow_weather(city: str, base_url: str) -> dict:
    geo_resp = requests.get(GEOCODING_URL, params={"name": city, "count": 1}, timeout=10)
    geo_resp.raise_for_status()
    results = geo_resp.json().get("results")
    if not results:
        raise ValueError(f"City '{city}' not found")

    lat, lon = results[0]["latitude"], results[0]["longitude"]
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,wind_speed_10m_max,precipitation_probability_max",
        "timezone": "auto",
        "start_date": tomorrow,
        "end_date": tomorrow,
    }
    resp = requests.get(f"{base_url}/v1/forecast", params=params, timeout=10)
    resp.raise_for_status()
    daily = resp.json()["daily"]

    wmo = daily["weather_code"][0]
    return {
        "date": tomorrow,
        "conditions": WMO_CONDITIONS.get(wmo, f"Code {wmo}"),
        "temperature_min_c": daily["temperature_2m_min"][0],
        "temperature_max_c": daily["temperature_2m_max"][0],
        "precipitation_probability_percent": daily["precipitation_probability_max"][0],
        "wind_kmh": daily["wind_speed_10m_max"][0],
    }
