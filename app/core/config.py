from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings / Configuration
    Yeh class environment variables (.env file) se settings load karti hai.
    Agar .env file na mile to default values use hongi taake application crash na ho.
    """

    # 1. App Information
    PROJECT_NAME: str = "Task Pulse API"
    API_V1_STR: str = "/api/v1"

    # 2. Database Connection
    # Default SQLite rakha hai taake beginners ko PostgreSQL setup ke baghair project run karne me asani ho
    # Agar PostgreSQL use karna ho to .env file me DATABASE_URL set karein
    DATABASE_URL: str = "sqlite:///./taskpulse.db"

    # 3. JWT Security Settings
    SECRET_KEY: str = "taskpulse-dev-secret-key-please-change-in-production-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 din (24 ghante)

    # Pydantic Settings Config:
    # Root directory ya app folder dono se .env file dhoondega
    model_config = SettingsConfigDict(
        env_file=(".env", "app/.env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Globally accessible settings instance
settings = Settings()
