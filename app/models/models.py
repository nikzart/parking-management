from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class Vehicle(Base):
    """Vehicle model."""
    __tablename__ = "vehicles"
    __table_args__ = (
        UniqueConstraint('number_plate', name='uq_vehicle_number_plate'),
    )

    id = Column(Integer, primary_key=True, index=True)
    number_plate = Column(String(20), nullable=False)
    contact_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    entry_timestamp = Column(DateTime, nullable=False)


class SystemConfig(Base):
    """System configuration model."""
    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True, index=True)
    retention_hours = Column(Integer, nullable=False, default=24)


class AuditLog(Base):
    """Audit log model."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(50), nullable=False)
    entity = Column(String(50), nullable=False)
    entity_id = Column(String(50), nullable=False)
    details = Column(String(500))
    timestamp = Column(DateTime, nullable=False)