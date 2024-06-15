from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent  # ..\osint-backend\src


class Settings(BaseSettings):
    PORT: int = 8000
    PROJECT_NAME: str = "telequiz"

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "telequizdb"
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"
    #DB_URL: str = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    #DB_URL: str = f"postgresql://{DB_USERNAME}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DB_URL: str = f"sqlite+aiosqlite:///./{DB_NAME}.db"
    #DB_ECHO: bool = False
    DB_ECHO: bool = True
    # JWT
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    EXPIRE_MINUTES: int = 1440  # 24 hours

    # Telegram Bot
    TOKEN: str = "7253524799:AAH262DWMzcJOPMwjlVVH6JkCL5Ir0jNWPI"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    REDIS_QUEUE_NAME: str = "telegram_queue"

    class Config:
        env_file = ".env"


settings = Settings()