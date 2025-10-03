from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import engine, get_db

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VNE Techwear Store API",
    description="Backend для интернет-магазина techwear бренда VNE",
    version="1.0.0"
)


# 1. Получение списка товаров
@app.get("/products", response_model=List[schemas.ProductBase])
def get_products(
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = Query(None, description="Фильтр по категории"),
        name: Optional[str] = Query(None, description="Поиск по названию"),
        db: Session = Depends(get_db)
):
    """
    Получить список товаров с возможностью фильтрации по категории и поиска по названию
    """
    query = db.query(models.Product)

    # Фильтрация по категории
    if category:
        query = query.filter(models.Product.category == category)

    # Поиск по названию (регистронезависимый)
    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))

    products = query.offset(skip).limit(limit).all()
    return products


# 2. Получение одного товара
@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Получить полную информацию о товаре по ID
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# 3. Добавление нового товара
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Добавить новый товар
    """
    # валидация
    if not product.name or not product.price:
        raise HTTPException(status_code=400, detail="Name and price are required")

    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be positive")

    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# 4. Удаление товара
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Удалить товар по ID
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}


@app.get("/")
def root():
    return {"message": "VNE Techwear Store API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)