from typing import Any, List
from decimal import Decimal
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import crud
from app.api import deps
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.budget import Budget
from pydantic import BaseModel

router = APIRouter()


class ExpenseByCategory(BaseModel):
    category_name: str
    category_icon: str
    category_color: str
    total: Decimal


class DashboardSummary(BaseModel):
    total_balance: Decimal
    total_accounts: int
    total_transactions: int
    total_budget: Decimal
    total_spent: Decimal
    budget_remaining: Decimal
    recent_transactions: list
    expense_by_category: List[ExpenseByCategory]


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get dashboard summary for current user."""

    # CRITICAL: Server-side calculation of total balance
    total_balance = db.query(func.sum(Account.balance)).filter(
        Account.user_id == current_user.id
    ).scalar() or Decimal("0.00")

    # Count accounts
    total_accounts = db.query(Account).filter(
        Account.user_id == current_user.id
    ).count()

    # Count transactions
    total_transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).count()

    # Get recent transactions (last 10)
    recent_transactions_query = crud.transaction.get_recent_transactions(
        db, user_id=current_user.id, limit=10
    )

    # Format transactions for response
    recent_transactions = [
        {
            "id": t.id,
            "amount": t.amount,
            "description": t.description,
            "transaction_type": t.transaction_type,
            "transaction_date": t.transaction_date,
            "merchant": t.merchant,
        }
        for t in recent_transactions_query
    ]

    # Get expense breakdown by category
    expense_breakdown = (
        db.query(
            Category.name,
            Category.icon,
            Category.color,
            func.sum(Transaction.amount).label("total")
        )
        .join(Transaction, Transaction.category_id == Category.id)
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "expense"
        )
        .group_by(Category.id, Category.name, Category.icon, Category.color)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(10)
        .all()
    )

    expense_by_category = [
        ExpenseByCategory(
            category_name=row.name,
            category_icon=row.icon or "📊",
            category_color=row.color or "#C4C4C4",
            total=row.total or Decimal("0.00")
        )
        for row in expense_breakdown
    ]

    # Calculate budget summary
    budgets = db.query(Budget).filter(Budget.user_id == current_user.id).all()

    total_budget = Decimal("0.00")
    total_spent = Decimal("0.00")

    for budget in budgets:
        total_budget += budget.amount

        # Calculate spent amount for this budget period
        if budget.period == "monthly":
            end_date = budget.start_date + timedelta(days=30)
        else:
            end_date = budget.start_date + timedelta(days=365)

        spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.category_id == budget.category_id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= budget.start_date,
            Transaction.transaction_date <= end_date,
        ).scalar() or Decimal("0.00")

        total_spent += spent

    budget_remaining = total_budget - total_spent

    return {
        "total_balance": total_balance,
        "total_accounts": total_accounts,
        "total_transactions": total_transactions,
        "total_budget": total_budget,
        "total_spent": total_spent,
        "budget_remaining": budget_remaining,
        "recent_transactions": recent_transactions,
        "expense_by_category": expense_by_category,
    }
