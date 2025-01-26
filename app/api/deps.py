from typing import Generator, Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.database import SessionLocal
from app.services.services import config_service

# API Key security scheme
api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)

def get_db() -> Generator:
    """
    Database session dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_api_key(
    api_key: str = Security(api_key_header)
) -> str:
    """
    Verify API key and return it if valid.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    if api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key

def get_retention_hours(
    db: Session = Depends(get_db)
) -> int:
    """
    Get current retention period from system config.
    """
    config = config_service.get_config(db)
    return config.retention_hours

class RateLimiter:
    """
    Simple in-memory rate limiter.
    In production, use Redis or similar for distributed rate limiting.
    """
    def __init__(self):
        self.requests = {}
        self.cleanup_interval = timedelta(minutes=1)
        self.last_cleanup = datetime.utcnow()

    def _cleanup_old_requests(self):
        """Remove expired request records."""
        now = datetime.utcnow()
        if now - self.last_cleanup > self.cleanup_interval:
            cutoff = now - timedelta(minutes=1)
            self.requests = {
                key: [ts for ts in timestamps if ts > cutoff]
                for key, timestamps in self.requests.items()
            }
            self.requests = {
                key: timestamps
                for key, timestamps in self.requests.items()
                if timestamps
            }
            self.last_cleanup = now

    def is_allowed(self, key: str) -> bool:
        """
        Check if request is allowed under rate limit.
        """
        self._cleanup_old_requests()
        now = datetime.utcnow()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove requests older than 1 minute
        self.requests[key] = [
            ts for ts in self.requests[key]
            if now - ts < timedelta(minutes=1)
        ]
        
        # Check rate limit
        if len(self.requests[key]) >= settings.RATE_LIMIT_PER_MINUTE:
            return False
        
        # Add new request
        self.requests[key].append(now)
        return True

# Create rate limiter instance
rate_limiter = RateLimiter()

async def check_rate_limit(
    api_key: str = Security(api_key_header)
) -> None:
    """
    Rate limiting dependency.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    if not rate_limiter.is_allowed(api_key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )