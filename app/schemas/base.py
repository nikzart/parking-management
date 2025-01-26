from pydantic import BaseModel, ConfigDict


class Pagination(BaseModel):
    """Base pagination schema."""
    total: int
    skip: int
    limit: int
    current_page: int
    total_pages: int
    total_items: int
    per_page: int

    @classmethod
    def from_params(cls, total: int, skip: int, limit: int) -> "Pagination":
        """Create pagination from parameters."""
        current_page = (skip // limit) + 1
        total_pages = (total + limit - 1) // limit
        return cls(
            total=total,
            skip=skip,
            limit=limit,
            current_page=current_page,
            total_pages=total_pages,
            total_items=total,
            per_page=limit
        )

    model_config = ConfigDict(from_attributes=True)