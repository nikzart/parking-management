from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
from fastapi import HTTPException
from datetime import datetime

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all services providing common CRUD operations.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a record by id."""
        query = select(self.model).where(self.model.id == id)
        result = db.execute(query).scalar_one_or_none()
        return result

    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        """Get a record by a specific field value."""
        query = select(self.model).where(getattr(self.model, field) == value)
        result = db.execute(query).scalar_one_or_none()
        return result

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "id",
        order: str = "desc"
    ) -> tuple[List[ModelType], int]:
        """
        Get a list of records with pagination.
        Returns tuple of (items, total_count).
        """
        # Get total count
        count_query = select(func.count()).select_from(self.model)
        total = db.execute(count_query).scalar()

        # Get items
        query = select(self.model)
        
        # Handle ordering
        order_column = getattr(self.model, order_by)
        if order.lower() == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        result = db.execute(query).scalars().all()
        return result, total

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        """Update a record."""
        obj_data = db_obj.to_dict()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: Any) -> ModelType:
        """Delete a record."""
        obj = self.get(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Record not found")
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session) -> int:
        """Get total count of records."""
        query = select(func.count()).select_from(self.model)
        return db.execute(query).scalar()

    def exists(self, db: Session, id: Any) -> bool:
        """Check if a record exists."""
        query = select(func.count()).select_from(self.model).where(self.model.id == id)
        return db.execute(query).scalar() > 0