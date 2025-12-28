from typing import Any, List
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.savings_goal import SavingsGoal, SavingsGoalCreate, SavingsGoalUpdate
from pydantic import BaseModel

router = APIRouter()


class SavingsGoalWithProgress(BaseModel):
    id: int
    user_id: int
    goal_name: str
    target_amount: Decimal
    current_amount: Decimal
    deadline: str | None
    icon: str | None
    created_at: str
    updated_at: str
    progress_percentage: float
    remaining: Decimal

    class Config:
        from_attributes = True


@router.get("/", response_model=List[SavingsGoalWithProgress])
def read_savings_goals(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get all savings goals for current user with progress calculation."""
    goals = crud.savings_goal.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )

    return [
        SavingsGoalWithProgress(
            id=goal.id,
            user_id=goal.user_id,
            goal_name=goal.goal_name,
            target_amount=goal.target_amount,
            current_amount=goal.current_amount,
            deadline=goal.deadline.isoformat() if goal.deadline else None,
            icon=goal.icon,
            created_at=goal.created_at.isoformat(),
            updated_at=goal.updated_at.isoformat(),
            progress_percentage=float((goal.current_amount / goal.target_amount) * 100) if goal.target_amount > 0 else 0,
            remaining=goal.target_amount - goal.current_amount,
        )
        for goal in goals
    ]


@router.post("/", response_model=SavingsGoal, status_code=status.HTTP_201_CREATED)
def create_savings_goal(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    goal_in: SavingsGoalCreate,
) -> Any:
    """Create new savings goal."""
    goal = crud.savings_goal.create_with_user(
        db, obj_in=goal_in, user_id=current_user.id
    )
    return goal


@router.get("/{goal_id}", response_model=SavingsGoalWithProgress)
def read_savings_goal(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    goal_id: int,
) -> Any:
    """Get savings goal by ID with progress calculation."""
    goal = crud.savings_goal.get_user_goal(
        db, goal_id=goal_id, user_id=current_user.id
    )
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Savings goal not found",
        )

    return SavingsGoalWithProgress(
        id=goal.id,
        user_id=goal.user_id,
        goal_name=goal.goal_name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        deadline=goal.deadline.isoformat() if goal.deadline else None,
        icon=goal.icon,
        created_at=goal.created_at.isoformat(),
        updated_at=goal.updated_at.isoformat(),
        progress_percentage=float((goal.current_amount / goal.target_amount) * 100) if goal.target_amount > 0 else 0,
        remaining=goal.target_amount - goal.current_amount,
    )


@router.put("/{goal_id}", response_model=SavingsGoal)
def update_savings_goal(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    goal_id: int,
    goal_in: SavingsGoalUpdate,
) -> Any:
    """Update savings goal."""
    goal = crud.savings_goal.get_user_goal(
        db, goal_id=goal_id, user_id=current_user.id
    )
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Savings goal not found",
        )

    goal = crud.savings_goal.update(db, db_obj=goal, obj_in=goal_in)
    return goal


@router.delete("/{goal_id}")
def delete_savings_goal(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    goal_id: int,
) -> Any:
    """Delete savings goal."""
    goal = crud.savings_goal.get_user_goal(
        db, goal_id=goal_id, user_id=current_user.id
    )
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Savings goal not found",
        )

    crud.savings_goal.delete(db, id=goal_id)
    return {"message": "Savings goal deleted successfully"}
