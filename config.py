import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class CommonSettings(BaseSettings):
    APP_NAME: str = "E-Commerce"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    # HOST: str = '0.0.0.0'
    HOST: str = 'localhost'
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = os.environ.get("DB_URL")
    DB_NAME: str = os.environ.get("DB_NAME")


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
