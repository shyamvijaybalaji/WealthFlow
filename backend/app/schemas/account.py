from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


# Shared properties
class AccountBase(BaseModel):
    account_name: str
    account_type: str  # checking, savings, credit_card, investment
    balance: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    currency: str = "USD"


# Properties to receive via API on creation
class AccountCreate(AccountBase):
    pass


# Properties to receive via API on update
class AccountUpdate(BaseModel):
    account_name: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[Decimal] = None
    currency: Optional[str] = None


# Additional properties stored in DB
class AccountInDBBase(AccountBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Account(AccountInDBBase):
    pass
