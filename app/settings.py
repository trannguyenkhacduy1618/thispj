from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    # Database
    DATABASE_URL: PostgresDsn

    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 giờ

    # App settings
    APP_NAME: str = "Time Tracking App"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
