from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


class CRUDBudget(CRUDBase[Budget, BudgetCreate, BudgetUpdate]):
    """CRUD operations for Budget model."""

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Budget]:
        """Get all budgets for a specific user."""
        return (
            db.query(Budget)
            .filter(Budget.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_budget(
        self, db: Session, *, budget_id: int, user_id: int
    ) -> Optional[Budget]:
        """Get a specific budget for a user (with ownership check)."""
        return (
            db.query(Budget)
            .filter(Budget.id == budget_id, Budget.user_id == user_id)
            .first()
        )

    def get_by_category(
        self, db: Session, *, category_id: int, user_id: int
    ) -> Optional[Budget]:
        """Get budget for a specific category and user."""
        return (
            db.query(Budget)
            .filter(Budget.category_id == category_id, Budget.user_id == user_id)
            .first()
        )

    def create_with_user(
        self, db: Session, *, obj_in: BudgetCreate, user_id: int
    ) -> Budget:
        """Create a budget for a specific user."""
        db_obj = Budget(
            **obj_in.model_dump(),
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


budget = CRUDBudget(Budget)
