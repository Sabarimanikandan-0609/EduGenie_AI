from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    app_env: str = "development"

    gemini_api_key: str = "AQ.Ab8RN6L8sjAWhK1vqFDuaGzE1HV7p3VVYUXixnBQ0aNxZfgL6Q"
    gemini_model: str = "gemini-3.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()