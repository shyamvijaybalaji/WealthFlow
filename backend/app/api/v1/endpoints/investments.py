from typing import Any, List
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.investment import Investment, InvestmentCreate, InvestmentUpdate
from pydantic import BaseModel

router = APIRouter()


class InvestmentWithROI(BaseModel):
    id: int
    user_id: int
    asset_type: str
    symbol: str
    quantity: Decimal
    purchase_price: Decimal
    current_price: Decimal | None
    purchase_date: str
    created_at: str
    updated_at: str
    total_cost: Decimal
    current_value: Decimal
    profit_loss: Decimal
    roi_percentage: float

    class Config:
        from_attributes = True


class PortfolioSummary(BaseModel):
    total_invested: Decimal
    current_value: Decimal
    total_profit_loss: Decimal
    roi_percentage: float
    investments_by_type: dict


def calculate_investment_roi(investment: Investment) -> InvestmentWithROI:
    """Calculate ROI for an investment."""
    total_cost = investment.quantity * investment.purchase_price

    if investment.current_price:
        current_value = investment.quantity * investment.current_price
        profit_loss = current_value - total_cost
        roi_percentage = float((profit_loss / total_cost) * 100) if total_cost > 0 else 0
    else:
        current_value = total_cost
        profit_loss = Decimal("0.00")
        roi_percentage = 0.0

    return InvestmentWithROI(
        id=investment.id,
        user_id=investment.user_id,
        asset_type=investment.asset_type,
        symbol=investment.symbol,
        quantity=investment.quantity,
        purchase_price=investment.purchase_price,
        current_price=investment.current_price,
        purchase_date=investment.purchase_date.isoformat(),
        created_at=investment.created_at.isoformat(),
        updated_at=investment.updated_at.isoformat(),
        total_cost=total_cost,
        current_value=current_value,
        profit_loss=profit_loss,
        roi_percentage=roi_percentage,
    )


@router.get("/", response_model=List[InvestmentWithROI])
def read_investments(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get all investments for current user with ROI calculation."""
    investments = crud.investment.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )

    return [calculate_investment_roi(inv) for inv in investments]


@router.get("/summary", response_model=PortfolioSummary)
def get_portfolio_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get portfolio summary with total ROI."""
    investments = crud.investment.get_by_user(db, user_id=current_user.id)

    total_invested = Decimal("0.00")
    current_value = Decimal("0.00")
    investments_by_type = {}

    for inv in investments:
        cost = inv.quantity * inv.purchase_price
        value = inv.quantity * inv.current_price if inv.current_price else cost

        total_invested += cost
        current_value += value

        # Group by asset type
        if inv.asset_type not in investments_by_type:
            investments_by_type[inv.asset_type] = {
                "count": 0,
                "total_value": 0.0
            }
        investments_by_type[inv.asset_type]["count"] += 1
        investments_by_type[inv.asset_type]["total_value"] += float(value)

    total_profit_loss = current_value - total_invested
    roi_percentage = float((total_profit_loss / total_invested) * 100) if total_invested > 0 else 0

    return PortfolioSummary(
        total_invested=total_invested,
        current_value=current_value,
        total_profit_loss=total_profit_loss,
        roi_percentage=roi_percentage,
        investments_by_type=investments_by_type,
    )


@router.post("/", response_model=Investment, status_code=status.HTTP_201_CREATED)
def create_investment(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    investment_in: InvestmentCreate,
) -> Any:
    """Create new investment."""
    investment = crud.investment.create_with_user(
        db, obj_in=investment_in, user_id=current_user.id
    )
    return investment


@router.get("/{investment_id}", response_model=InvestmentWithROI)
def read_investment(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    investment_id: int,
) -> Any:
    """Get investment by ID with ROI calculation."""
    investment = crud.investment.get_user_investment(
        db, investment_id=investment_id, user_id=current_user.id
    )
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )

    return calculate_investment_roi(investment)


@router.put("/{investment_id}", response_model=Investment)
def update_investment(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    investment_id: int,
    investment_in: InvestmentUpdate,
) -> Any:
    """Update investment."""
    investment = crud.investment.get_user_investment(
        db, investment_id=investment_id, user_id=current_user.id
    )
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )

    investment = crud.investment.update(db, db_obj=investment, obj_in=investment_in)
    return investment


@router.delete("/{investment_id}")
def delete_investment(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    investment_id: int,
) -> Any:
    """Delete investment."""
    investment = crud.investment.get_user_investment(
        db, investment_id=investment_id, user_id=current_user.id
    )
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )

    crud.investment.delete(db, id=investment_id)
    return {"message": "Investment deleted successfully"}
