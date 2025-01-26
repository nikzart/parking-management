from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


class TimestampMixin:
    """Mixin for adding timestamp fields."""
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)