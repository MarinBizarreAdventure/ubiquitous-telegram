import json

import anthropic

from app.domain.entities import Place, Recommendation, WeatherForecast
from app.domain.ports import AIAgentPort


class ClaudeAgent(AIAgentPort):
    def __init__(self, api_key: str) -> None:
        self._client = anthropic.Anthropic(api_key=api_key)

    def get_recommendation(
        self,
        user_message: str,
        weather: WeatherForecast,
        places: list[Place],
        history: list[dict],
    ) -> Recommendation:
        system_prompt = (
            "You are a helpful city guide assistant. "
            "Your job is to suggest places to go out and what to wear based on tomorrow's weather. "
            "Always respond in JSON with this exact structure: "
            '{"places": [{"name": "", "type": "", "location": "", "description": "", "url": "", "rating": ""}], '
            '"outfit_suggestion": "", "reasoning": ""}'
        )

        weather_context = (
            f"Tomorrow's weather in the user's city: {weather.conditions}, "
            f"min {weather.temperature_min}°C / max {weather.temperature_max}°C, "
            f"humidity {weather.humidity}%, wind {weather.wind_speed} km/h."
        )

        places_context = "Available places found:\n" + "\n".join(
            f"- {p.name} ({p.type}): {p.description}" for p in places
        ) if places else "No specific places found, use your knowledge."

        messages = [
            *history,
            {
                "role": "user",
                "content": (
                    f"{weather_context}\n\n{places_context}\n\n"
                    f"User request: {user_message}"
                ),
            },
        ]

        response = self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )

        raw = response.content[0].text
        data = json.loads(raw)

        return Recommendation(
            places=[Place(**p) for p in data.get("places", [])],
            outfit_suggestion=data.get("outfit_suggestion", ""),
            reasoning=data.get("reasoning", ""),
        )
