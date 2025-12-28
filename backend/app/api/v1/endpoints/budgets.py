from typing import Any, List
from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app import crud
from app.api import deps
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.budget import Budget, BudgetCreate, BudgetUpdate
from pydantic import BaseModel

router = APIRouter()


class BudgetWithSpending(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: Decimal
    period: str
    alert_threshold: float
    start_date: datetime
    created_at: datetime
    updated_at: datetime
    spent: Decimal
    remaining: Decimal
    percentage: float
    status: str  # ok, warning, exceeded

    class Config:
        from_attributes = True


def calculate_budget_spending(db: Session, budget: Budget, user_id: int) -> BudgetWithSpending:
    """Calculate spending for a budget period."""
    # Calculate period end date
    if budget.period == "monthly":
        end_date = budget.start_date + timedelta(days=30)
    elif budget.period == "yearly":
        end_date = budget.start_date + timedelta(days=365)
    else:
        end_date = datetime.utcnow()

    # CRITICAL: Server-side calculation of spending
    spent = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.user_id == user_id,
            Transaction.category_id == budget.category_id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= budget.start_date,
            Transaction.transaction_date <= end_date,
        )
    ).scalar() or Decimal("0.00")

    remaining = budget.amount - spent
    percentage = float((spent / budget.amount) * 100) if budget.amount > 0 else 0

    # Determine status
    if percentage >= 100:
        status = "exceeded"
    elif percentage >= (budget.alert_threshold * 100):
        status = "warning"
    else:
        status = "ok"

    return BudgetWithSpending(
        id=budget.id,
        user_id=budget.user_id,
        category_id=budget.category_id,
        amount=budget.amount,
        period=budget.period,
        alert_threshold=budget.alert_threshold,
        start_date=budget.start_date,
        created_at=budget.created_at,
        updated_at=budget.updated_at,
        spent=spent,
        remaining=remaining,
        percentage=percentage,
        status=status,
    )


@router.get("/", response_model=List[BudgetWithSpending])
def read_budgets(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get all budgets for current user with spending calculation."""
    budgets = crud.budget.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )

    return [calculate_budget_spending(db, budget, current_user.id) for budget in budgets]


@router.post("/", response_model=Budget, status_code=status.HTTP_201_CREATED)
def create_budget(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    budget_in: BudgetCreate,
) -> Any:
    """Create new budget."""
    # Verify category exists and user has access
    category = crud.category.get_user_category(
        db, category_id=budget_in.category_id, user_id=current_user.id
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    # Check if budget already exists for this category
    existing_budget = crud.budget.get_by_category(
        db, category_id=budget_in.category_id, user_id=current_user.id
    )
    if existing_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Budget already exists for category '{category.name}'. Please update the existing budget instead.",
        )

    budget = crud.budget.create_with_user(
        db, obj_in=budget_in, user_id=current_user.id
    )
    return budget


@router.get("/{budget_id}", response_model=BudgetWithSpending)
def read_budget(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    budget_id: int,
) -> Any:
    """Get budget by ID with spending calculation."""
    budget = crud.budget.get_user_budget(
        db, budget_id=budget_id, user_id=current_user.id
    )
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found",
        )

    return calculate_budget_spending(db, budget, current_user.id)


@router.put("/{budget_id}", response_model=Budget)
def update_budget(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    budget_id: int,
    budget_in: BudgetUpdate,
) -> Any:
    """Update budget."""
    budget = crud.budget.get_user_budget(
        db, budget_id=budget_id, user_id=current_user.id
    )
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found",
        )

    budget = crud.budget.update(db, db_obj=budget, obj_in=budget_in)
    return budget


@router.delete("/{budget_id}")
def delete_budget(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    budget_id: int,
) -> Any:
    """Delete budget."""
    budget = crud.budget.get_user_budget(
        db, budget_id=budget_id, user_id=current_user.id
    )
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found",
        )

    crud.budget.delete(db, id=budget_id)
    return {"message": "Budget deleted successfully"}
