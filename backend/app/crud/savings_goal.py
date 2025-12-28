from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.savings_goal import SavingsGoal
from app.schemas.savings_goal import SavingsGoalCreate, SavingsGoalUpdate


class CRUDSavingsGoal(CRUDBase[SavingsGoal, SavingsGoalCreate, SavingsGoalUpdate]):
    """CRUD operations for SavingsGoal model."""

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[SavingsGoal]:
        """Get all savings goals for a specific user."""
        return (
            db.query(SavingsGoal)
            .filter(SavingsGoal.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_goal(
        self, db: Session, *, goal_id: int, user_id: int
    ) -> Optional[SavingsGoal]:
        """Get a specific savings goal for a user (with ownership check)."""
        return (
            db.query(SavingsGoal)
            .filter(SavingsGoal.id == goal_id, SavingsGoal.user_id == user_id)
            .first()
        )

    def create_with_user(
        self, db: Session, *, obj_in: SavingsGoalCreate, user_id: int
    ) -> SavingsGoal:
        """Create a savings goal for a specific user."""
        db_obj = SavingsGoal(
            **obj_in.model_dump(),
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


savings_goal = CRUDSavingsGoal(SavingsGoal)
