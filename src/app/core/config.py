import typing

import pytz
from pydantic_settings import BaseSettings

ROUTE_PREFIX_V1 = "/v1"

class Settings(BaseSettings):
    APP_TITLE: str = "Task Manager API"
    APP_DESCRIPTION: str = "REST API service for managing tasks"
    APP_VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    TIMEZONE: typing.ClassVar = pytz.timezone("Europe/Moscow")

    class Config:
        env_file = ".env"


settings = Settings()