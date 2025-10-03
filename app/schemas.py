from pydantic import BaseModel, ConfigDict
from typing import Optional

# Базовая схема для товара (для списка)
class ProductBase(BaseModel):
    id: int
    name: str
    price: float
    category: str

    model_config = ConfigDict(from_attributes=True)

# создания товара
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    sizes: Optional[str] = None

# Полная схема товара
class Product(ProductBase):
    description: Optional[str] = None
    sizes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)