from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
PROJECT_NAME: str = "Time Tracking Backend"


# Security
SECRET_KEY: str = "CHANGE_ME"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


# Database
DATABASE_URL: str


# CORS
BACKEND_CORS_ORIGINS: List[str] = ["*"]


class Config:
env_file = ".env"


settings = Settings()
