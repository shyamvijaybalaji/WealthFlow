from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.investment import Investment
from app.schemas.investment import InvestmentCreate, InvestmentUpdate


class CRUDInvestment(CRUDBase[Investment, InvestmentCreate, InvestmentUpdate]):
    """CRUD operations for Investment model."""

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Investment]:
        """Get all investments for a specific user."""
        return (
            db.query(Investment)
            .filter(Investment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_investment(
        self, db: Session, *, investment_id: int, user_id: int
    ) -> Optional[Investment]:
        """Get a specific investment for a user (with ownership check)."""
        return (
            db.query(Investment)
            .filter(Investment.id == investment_id, Investment.user_id == user_id)
            .first()
        )

    def create_with_user(
        self, db: Session, *, obj_in: InvestmentCreate, user_id: int
    ) -> Investment:
        """Create an investment for a specific user."""
        db_obj = Investment(
            **obj_in.model_dump(),
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


investment = CRUDInvestment(Investment)
