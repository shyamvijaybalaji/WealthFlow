from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from app.crud.base import CRUDBase
from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    """CRUD operations for Transaction model."""

    def get_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        account_id: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> List[Transaction]:
        """Get all transactions for a user with optional filters."""
        query = db.query(Transaction).filter(Transaction.user_id == user_id)

        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)

        return (
            query.order_by(desc(Transaction.transaction_date))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_transaction(
        self, db: Session, *, transaction_id: int, user_id: int
    ) -> Optional[Transaction]:
        """Get a specific transaction for a user (with ownership check)."""
        return (
            db.query(Transaction)
            .filter(
                Transaction.id == transaction_id, Transaction.user_id == user_id
            )
            .first()
        )

    def create_with_user(
        self, db: Session, *, obj_in: TransactionCreate, user_id: int
    ) -> Transaction:
        """Create a transaction and update account balance."""
        # CRITICAL: Verify account ownership
        account = (
            db.query(Account)
            .filter(Account.id == obj_in.account_id, Account.user_id == user_id)
            .first()
        )
        if not account:
            raise ValueError("Account not found or access denied")

        # Create transaction
        db_obj = Transaction(
            **obj_in.model_dump(),
            user_id=user_id,
        )
        db.add(db_obj)

        # Update account balance
        # CRITICAL: Server-side calculation using Decimal
        amount = Decimal(str(obj_in.amount))
        if obj_in.transaction_type == "income":
            account.balance += amount
        elif obj_in.transaction_type == "expense":
            account.balance -= amount
        # Note: transfers handled separately

        db.add(account)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_recent_transactions(
        self, db: Session, *, user_id: int, limit: int = 10
    ) -> List[Transaction]:
        """Get recent transactions for dashboard."""
        return (
            db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(desc(Transaction.transaction_date))
            .limit(limit)
            .all()
        )


transaction = CRUDTransaction(Transaction)
