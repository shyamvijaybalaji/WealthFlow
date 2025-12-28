from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


# Shared properties
class SavingsGoalBase(BaseModel):
    goal_name: str
    target_amount: Decimal = Field(decimal_places=2)
    current_amount: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    deadline: Optional[datetime] = None
    icon: Optional[str] = None


# Properties to receive via API on creation
class SavingsGoalCreate(SavingsGoalBase):
    pass


# Properties to receive via API on update
class SavingsGoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    target_amount: Optional[Decimal] = None
    current_amount: Optional[Decimal] = None
    deadline: Optional[datetime] = None
    icon: Optional[str] = None


# Additional properties stored in DB
class SavingsGoalInDBBase(SavingsGoalBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class SavingsGoal(SavingsGoalInDBBase):
    pass
