"""OpenBerg Terminal — server settings via pydantic-settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from env vars / .env file."""

    finnhub_api_key: str = ""
    database_url: str = "sqlite:///data/openberg.db"
    data_provider: str = Field(
        default="auto",
        description="auto, mock, yahoo, or finnhub",
    )
    cache_quotes_ttl: int = 10
    cache_prices_ttl: int = 60
    cache_security_ttl: int = 300
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="OPENBERG_",
        case_sensitive=False,
    )


# Module-level singleton — import this wherever settings are needed.
settings = Settings()


def load_settings() -> Settings:
    """Return the module-level Settings instance.

    Callers can use this function to make it explicit that settings are
    lazily loaded from the environment at first import time.
    """
    return settings
