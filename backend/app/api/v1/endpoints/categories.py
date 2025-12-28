from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.category import Category

router = APIRouter()


@router.get("/", response_model=List[Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get all categories for current user (system + user-specific)."""
    categories = crud.category.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return categories
