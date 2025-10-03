from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from ..database import get_db
from ..models import Product
from ..schemas import ProductBase, Product, ProductCreate

router = APIRouter()


@router.get("/products", response_model=List[ProductBase])
async def get_products(
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = Query(None, description="Фильтр по категории"),
        name: Optional[str] = Query(None, description="Поиск по названию"),
        db: AsyncSession = Depends(get_db)
):
    """
    Получить список товаров с возможностью фильтрации по категории и поиска по названию
    """
    query = select(Product)

    if category:
        query = query.where(Product.category == category)

    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))

    result = await db.execute(query.offset(skip).limit(limit))
    products = result.scalars().all()
    return products


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить полную информацию о товаре по ID
    """
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=Product)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Добавить новый товар
    """
    # Валидация выполнена в Pydantic схеме
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удалить товар по ID
    """
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {"message": "Product deleted successfully"}