from fastapi import APIRouter, Depends, HTTPException

from app.adapters.api.schemas import WeatherResponse
from app.container import get_weather_use_case
from app.use_cases.weather import WeatherUseCase

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/{city}", response_model=WeatherResponse)
def get_weather(city: str, uc: WeatherUseCase = Depends(get_weather_use_case)):
    try:
        forecast = uc.get_tomorrow_forecast(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather service error: {str(e)}")
    return WeatherResponse(
        date=forecast.date,
        temperature_min=forecast.temperature_min,
        temperature_max=forecast.temperature_max,
        conditions=forecast.conditions,
        humidity=forecast.humidity,
        wind_speed=forecast.wind_speed,
    )
