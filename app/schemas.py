from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    sizes: Optional[str] = Field(None, max_length=100)


class ProductResponse(ProductBase):
    description: Optional[str] = None
    sizes: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
