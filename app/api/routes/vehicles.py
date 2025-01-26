from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas import schemas
from app.services.services import vehicle_service
from app.api.deps import get_db, verify_api_key, check_rate_limit
from app.schemas.base import Pagination

router = APIRouter()


@router.post(
    "",
    response_model=schemas.VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def create_vehicle(
    vehicle_in: schemas.VehicleCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new vehicle entry.
    """
    return vehicle_service.create_vehicle(db, vehicle_in)


@router.get(
    "",
    response_model=schemas.VehicleList,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def list_vehicles(
    skip: int = 0,
    limit: int = 50,
    order_by: str = "entry_timestamp",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    """
    List all active vehicles with pagination.
    """
    vehicles, total = vehicle_service.list(db, skip, limit, order_by, order)
    return {
        "items": vehicles,
        "pagination": Pagination.from_params(total, skip, limit)
    }


@router.get(
    "/{number}",
    response_model=schemas.VehicleResponse,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def get_vehicle(
    number: str,
    db: Session = Depends(get_db)
):
    """
    Get vehicle details by number plate.
    """
    vehicle = vehicle_service.get_by_number_plate(db, number)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with number plate {number} not found"
        )
    return vehicle


@router.delete(
    "/{number}",
    response_model=schemas.VehicleResponse,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def remove_vehicle(
    number: str,
    db: Session = Depends(get_db)
):
    """
    Remove a vehicle entry.
    """
    return vehicle_service.remove_vehicle(db, number)


@router.get(
    "/search/{term}",
    response_model=schemas.VehicleList,
    dependencies=[Depends(verify_api_key), Depends(check_rate_limit)]
)
async def search_vehicles(
    term: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Search vehicles by number plate or contact name.
    """
    vehicles, total = vehicle_service.search_vehicles(db, term, skip, limit)
    return {
        "items": vehicles,
        "pagination": Pagination.from_params(total, skip, limit)
    }