from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):
    """CRUD operations for Account model."""

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Account]:
        """Get all accounts for a specific user."""
        return (
            db.query(Account)
            .filter(Account.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_account(
        self, db: Session, *, account_id: int, user_id: int
    ) -> Optional[Account]:
        """Get a specific account for a user (with ownership check)."""
        return (
            db.query(Account)
            .filter(Account.id == account_id, Account.user_id == user_id)
            .first()
        )

    def create_with_user(
        self, db: Session, *, obj_in: AccountCreate, user_id: int
    ) -> Account:
        """Create an account for a specific user."""
        db_obj = Account(
            **obj_in.model_dump(),
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


account = CRUDAccount(Account)
