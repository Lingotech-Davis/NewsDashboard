"""requirements.txt
pydantic_settings
"""

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
    POSTGRESQL_PWD: str

    model_config = SettingsConfigDict(env_file=".env")
