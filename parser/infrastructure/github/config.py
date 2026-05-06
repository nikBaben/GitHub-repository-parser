from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Конфигурация приложения.

    Загружает настройки из переменных окружения и `.env` файла,
    используя Pydantic Settings.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
    )

    TOKEN: str 
    GITHUB_URL: str
    GITHUB_API_URL: str = Field(default="https://api.github.com")
    GITHUB_API_VERSION: str = Field(default="2026-03-10")
    DEFAULT_TIMEOUT: int = Field(default=40)
    DEFAULT_PER_PAGE: int = Field(default=100)
    DEFAULT_RETRIES: int = Field(default=4)
    DAYS: int = Field(default=10)
    HISTORY_CACHE_TTL_SECONDS: int = Field(default=3600)


settings = Settings()  # pyright: ignore[reportCallIssue]
