from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    claude_api_key: str
    open_meteo_base_url: str = "https://api.open-meteo.com"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    data_dir: str = "./data"
    database_url: str | None = None


settings = Settings()
