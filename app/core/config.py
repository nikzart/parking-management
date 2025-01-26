from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    PROJECT_NAME: str = "Parking Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./parking_system.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # System Settings
    DEFAULT_RETENTION_HOURS: int = 24
    RATE_LIMIT_PER_MINUTE: int = 100
    MAX_WEBSOCKET_CONNECTIONS: int = 5
    
    # Monitoring
    GRAFANA_PASSWORD: str = "admin"
    
    # Development Settings
    DEBUG: bool = False
    RELOAD: bool = False
    TESTING: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )
    
    @field_validator("BACKEND_CORS_ORIGINS")
    def validate_cors_origins(cls, v: List[str]) -> List[str]:
        """Validate CORS origins."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v


settings = Settings()