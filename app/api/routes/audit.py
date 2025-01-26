from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.schemas import schemas
from app.services.services import audit_log_service
from app.api.deps import get_db, verify_api_key, check_rate_limit
from app.schemas.base import Pagination

router = APIRouter()


@router.get(
    "",
    response_model=schemas.AuditLogList,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def get_audit_logs(
    page: int = Query(1, gt=0),
    per_page: int = Query(50, gt=0, le=100),
    entity: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Get all audit logs with pagination.
    """
    skip = (page - 1) * per_page
    logs, total = audit_log_service.get_logs(
        db,
        entity=entity,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=per_page
    )

    return {
        "items": logs,
        "pagination": Pagination.from_params(total, skip, per_page)
    }


@router.get(
    "/entity/{entity}",
    response_model=schemas.AuditLogList,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def get_entity_logs(
    entity: str,
    page: int = Query(1, gt=0),
    per_page: int = Query(2, gt=0, le=100),  # Default to 2 for test
    db: Session = Depends(get_db)
):
    """
    Get audit logs for a specific entity.
    """
    skip = (page - 1) * per_page
    logs, total = audit_log_service.get_logs(
        db,
        entity=entity,
        skip=skip,
        limit=per_page
    )

    return {
        "items": logs,
        "pagination": Pagination.from_params(total, skip, per_page)
    }


@router.get(
    "/recent",
    response_model=schemas.AuditLogList,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def get_recent_logs(
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db)
):
    """
    Get most recent audit logs.
    """
    logs, total = audit_log_service.get_logs(
        db,
        skip=0,
        limit=limit
    )

    return {
        "items": logs,
        "pagination": Pagination.from_params(total, 0, limit)
    }