from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


# Shared properties
class TransactionBase(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    amount: Decimal = Field(decimal_places=2)
    description: str
    merchant: Optional[str] = None
    transaction_type: str  # income, expense, transfer
    transaction_date: datetime
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


# Properties to receive via API on creation
class TransactionCreate(TransactionBase):
    pass


# Properties to receive via API on update
class TransactionUpdate(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    merchant: Optional[str] = None
    transaction_type: Optional[str] = None
    transaction_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


# Additional properties stored in DB
class TransactionInDBBase(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Transaction(TransactionInDBBase):
    pass
