from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


# Shared properties
class InvestmentBase(BaseModel):
    asset_type: str  # stock, crypto, bond, etf, mutual_fund
    symbol: str
    quantity: Decimal = Field(decimal_places=8)
    purchase_price: Decimal = Field(decimal_places=2)
    current_price: Optional[Decimal] = Field(default=None, decimal_places=2)
    purchase_date: datetime


# Properties to receive via API on creation
class InvestmentCreate(InvestmentBase):
    pass


# Properties to receive via API on update
class InvestmentUpdate(BaseModel):
    asset_type: Optional[str] = None
    symbol: Optional[str] = None
    quantity: Optional[Decimal] = None
    purchase_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    purchase_date: Optional[datetime] = None


# Additional properties stored in DB
class InvestmentInDBBase(InvestmentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Investment(InvestmentInDBBase):
    pass
