from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# Shared properties
class CategoryBase(BaseModel):
    name: str
    category_type: str  # income, expense
    icon: Optional[str] = None
    color: Optional[str] = None


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive via API on update
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    category_type: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


# Additional properties stored in DB
class CategoryInDBBase(CategoryBase):
    id: int
    user_id: Optional[int] = None
    is_system: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Category(CategoryInDBBase):
    pass
