from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.models import Vehicle, SystemConfig, AuditLog
from app.schemas import schemas


class VehicleService:
    """Service for managing vehicles."""
    
    def get_by_number_plate(self, db: Session, number_plate: str) -> Optional[Vehicle]:
        """Get vehicle by number plate."""
        return db.query(Vehicle).filter(Vehicle.number_plate == number_plate).first()
    
    def create_vehicle(self, db: Session, vehicle_in: schemas.VehicleCreate) -> Vehicle:
        """Create a new vehicle entry with validation."""
        try:
            # Create vehicle
            vehicle = Vehicle(
                number_plate=vehicle_in.number_plate,
                contact_name=vehicle_in.contact_name,
                phone_number=vehicle_in.phone_number,
                entry_timestamp=datetime.utcnow()
            )
            db.add(vehicle)
            db.flush()  # Flush to get the ID but don't commit yet
            
            # Log the action
            AuditLogService.log_action(
                db,
                "CREATE",
                "Vehicle",
                str(vehicle.id),
                f"Vehicle {vehicle.number_plate} registered"
            )
            
            db.commit()
            db.refresh(vehicle)
            return vehicle
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vehicle with number plate {vehicle_in.number_plate} already exists"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def remove_vehicle(self, db: Session, number_plate: str) -> Vehicle:
        """Remove a vehicle by number plate."""
        vehicle = self.get_by_number_plate(db, number_plate)
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with number plate {number_plate} not found"
            )
        
        try:
            # Delete vehicle
            db.delete(vehicle)
            
            # Log the action
            AuditLogService.log_action(
                db,
                "DELETE",
                "Vehicle",
                str(vehicle.id),
                f"Vehicle {vehicle.number_plate} removed"
            )
            
            db.commit()
            return vehicle
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def search_vehicles(
        self,
        db: Session,
        search_term: str,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[Vehicle], int]:
        """Search vehicles by number plate or contact name."""
        query = db.query(Vehicle).filter(
            or_(
                Vehicle.number_plate.ilike(f"%{search_term}%"),
                Vehicle.contact_name.ilike(f"%{search_term}%")
            )
        )
        
        total = query.count()
        vehicles = query.offset(skip).limit(limit).all()
        
        return vehicles, total
    
    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 50,
        order_by: str = "entry_timestamp",
        order: str = "desc"
    ) -> Tuple[List[Vehicle], int]:
        """List vehicles with pagination."""
        query = db.query(Vehicle)
        
        # Apply ordering
        if order.lower() == "desc":
            query = query.order_by(getattr(Vehicle, order_by).desc())
        else:
            query = query.order_by(getattr(Vehicle, order_by).asc())
        
        total = query.count()
        vehicles = query.offset(skip).limit(limit).all()
        
        return vehicles, total
    
    def cleanup_expired_vehicles(self, db: Session) -> int:
        """Remove vehicles that have exceeded retention period."""
        config = SystemConfigService().get_config(db)
        retention_hours = config.retention_hours
        
        cutoff_time = datetime.utcnow() - timedelta(hours=retention_hours)
        query = db.query(Vehicle).filter(Vehicle.entry_timestamp < cutoff_time)
        
        vehicles = query.all()
        count = 0
        
        try:
            for vehicle in vehicles:
                db.delete(vehicle)
                count += 1
                
                AuditLogService.log_action(
                    db,
                    "DELETE",
                    "Vehicle",
                    str(vehicle.id),
                    f"Vehicle {vehicle.number_plate} removed due to retention policy"
                )
            
            db.commit()
            return count
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )


class SystemConfigService:
    """Service for managing system configuration."""
    
    def get_config(self, db: Session) -> SystemConfig:
        """Get current system configuration."""
        config = db.query(SystemConfig).first()
        if not config:
            config = SystemConfig(retention_hours=24)
            db.add(config)
            db.commit()
            db.refresh(config)
        return config
    
    def update_retention_period(
        self,
        db: Session,
        retention_hours: int
    ) -> SystemConfig:
        """Update data retention period."""
        try:
            config = self.get_config(db)
            config.retention_hours = retention_hours
            
            # Log the action
            AuditLogService.log_action(
                db,
                "UPDATE",
                "SystemConfig",
                str(config.id),
                f"Retention period updated to {retention_hours} hours"
            )
            
            db.commit()
            db.refresh(config)
            return config
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )


class AuditLogService:
    """Service for managing audit logs."""
    
    @staticmethod
    def log_action(
        db: Session,
        action: str,
        entity: str,
        entity_id: str,
        details: Optional[str] = None
    ) -> AuditLog:
        """Create an audit log entry."""
        log = AuditLog(
            action=action,
            entity=entity,
            entity_id=entity_id,
            details=details,
            timestamp=datetime.utcnow()
        )
        db.add(log)
        db.flush()  # Flush but don't commit, let the caller handle the transaction
        return log
    
    def get_logs(
        self,
        db: Session,
        *,
        entity: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[AuditLog], int]:
        """Get audit logs with filtering and pagination."""
        query = db.query(AuditLog)
        
        if entity:
            query = query.filter(AuditLog.entity == entity)
        if start_date:
            query = query.filter(AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(AuditLog.timestamp <= end_date)
        
        query = query.order_by(AuditLog.timestamp.desc())
        
        total = query.count()
        logs = query.offset(skip).limit(limit).all()
        
        return logs, total


# Create service instances
vehicle_service = VehicleService()
config_service = SystemConfigService()
audit_log_service = AuditLogService()