from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


# Shared properties
class BudgetBase(BaseModel):
    category_id: int
    amount: Decimal = Field(decimal_places=2)
    period: str  # monthly, yearly
    alert_threshold: float = 0.80
    start_date: datetime


# Properties to receive via API on creation
class BudgetCreate(BudgetBase):
    pass


# Properties to receive via API on update
class BudgetUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[Decimal] = None
    period: Optional[str] = None
    alert_threshold: Optional[float] = None
    start_date: Optional[datetime] = None


# Additional properties stored in DB
class BudgetInDBBase(BudgetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Budget(BudgetInDBBase):
    pass
