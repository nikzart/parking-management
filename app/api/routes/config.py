from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas import schemas
from app.services.services import config_service
from app.api.deps import get_db, verify_api_key, check_rate_limit
from app.models.models import Vehicle, SystemConfig

router = APIRouter()


@router.get(
    "/retention",
    response_model=schemas.SystemConfigResponse,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def get_retention_period(
    db: Session = Depends(get_db)
):
    """
    Get current data retention period.
    """
    return config_service.get_config(db)


@router.put(
    "/retention",
    response_model=schemas.SystemConfigResponse,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def update_retention_period(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Update data retention period.
    """
    try:
        body = await request.json()
        config_in = schemas.SystemConfigUpdate(**body)
        return config_service.update_retention_period(db, config_in.retention_hours)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/maintenance/clear",
    response_model=schemas.MaintenanceResponse,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def clear_database(
    request: schemas.MaintenanceRequest,
    db: Session = Depends(get_db)
):
    """
    Clear entire database. Requires confirmation message.
    """
    if request.confirmation != "I understand this will delete all data":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid confirmation message"
        )
    
    try:
        # Clear vehicles
        query = db.query(Vehicle)
        count = query.count()
        query.delete()
        
        # Reset system config to defaults
        config = config_service.get_config(db)
        config.retention_hours = 24
        
        db.commit()
        
        return {
            "message": "Database cleared successfully",
            "timestamp": datetime.utcnow(),
            "records_removed": count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )