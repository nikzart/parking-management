from typing import Optional
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Parking Management System"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    API_KEY_NAME: str = "X-API-Key"
    RATE_LIMIT_PER_MINUTE: int = 100
    MAX_WEBSOCKET_CONNECTIONS: int = 5
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./parking_system.db"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Metrics
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Testing
    TESTING: bool = bool(os.getenv("TESTING", False))

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()