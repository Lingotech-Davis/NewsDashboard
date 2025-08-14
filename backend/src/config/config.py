"""requirements.txt
pydantic_settings
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defining 3 main API keys:
    GEMINI_API_KEY
    NEWS_API_KEY
    POSTGRESQL_PWD
    """

    GEMINI_API_KEY: str
    NEWS_API_KEY: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    """
    Loads API keys and other settings, caching the result.
    """
    # returns settings object
    return Settings()  # type: ignore (making linter shut up)
