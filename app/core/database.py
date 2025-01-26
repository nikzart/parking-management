from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings

# Create SQLAlchemy engine
if settings.TESTING:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
else:
    SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

# Create engine with SQLite configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Database dependency
def get_db() -> Generator:
    """
    Database session dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()