from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    """CRUD operations for Category model."""

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        """Get all categories for a user (system + user-specific)."""
        return (
            db.query(Category)
            .filter(
                or_(Category.user_id == user_id, Category.is_system == True)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_category(
        self, db: Session, *, category_id: int, user_id: int
    ) -> Optional[Category]:
        """Get a specific category for a user (with ownership check)."""
        return (
            db.query(Category)
            .filter(
                Category.id == category_id,
                or_(Category.user_id == user_id, Category.is_system == True),
            )
            .first()
        )

    def create_with_user(
        self, db: Session, *, obj_in: CategoryCreate, user_id: int
    ) -> Category:
        """Create a category for a specific user."""
        db_obj = Category(
            **obj_in.model_dump(),
            user_id=user_id,
            is_system=False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_system_category(
        self, db: Session, *, obj_in: CategoryCreate
    ) -> Category:
        """Create a system-wide default category."""
        db_obj = Category(
            **obj_in.model_dump(),
            user_id=None,
            is_system=True,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


category = CRUDCategory(Category)
