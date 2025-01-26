from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, constr, field_validator, ConfigDict

from app.schemas.base import Pagination


class VehicleBase(BaseModel):
    """Base vehicle schema."""
    number_plate: constr(min_length=1, max_length=20)
    contact_name: constr(min_length=1, max_length=100)
    phone_number: constr(min_length=1, max_length=20)
    model_config = ConfigDict(from_attributes=True)


class VehicleCreate(VehicleBase):
    """Vehicle creation schema."""
    pass


class VehicleResponse(VehicleBase):
    """Vehicle response schema."""
    id: int
    entry_timestamp: datetime


class VehicleList(BaseModel):
    """Vehicle list schema."""
    items: List[VehicleResponse]
    pagination: Pagination


class SystemConfigBase(BaseModel):
    """Base system config schema."""
    retention_hours: int = Field(
        default=24,
        description="Data retention period in hours (1-168)",
        gt=0,
        le=168
    )
    model_config = ConfigDict(from_attributes=True)

    @field_validator('retention_hours')
    @classmethod
    def validate_retention_hours(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Retention period must be greater than 0")
        if v > 168:
            raise ValueError("Retention period cannot exceed 168 hours (1 week)")
        return v


class SystemConfigUpdate(SystemConfigBase):
    """System config update schema."""
    pass


class SystemConfigResponse(SystemConfigBase):
    """System config response schema."""
    id: int


class AuditLogBase(BaseModel):
    """Base audit log schema."""
    action: str
    entity: str
    entity_id: str
    details: Optional[str] = None
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class AuditLogResponse(AuditLogBase):
    """Audit log response schema."""
    id: int


class AuditLogList(BaseModel):
    """Audit log list schema."""
    items: List[AuditLogResponse]
    pagination: Pagination


class MaintenanceRequest(BaseModel):
    """Maintenance request schema."""
    confirmation: str = Field(
        description="Confirmation message to prevent accidental database clearing"
    )


class MaintenanceResponse(BaseModel):
    """Maintenance response schema."""
    message: str
    timestamp: datetime
    records_removed: int