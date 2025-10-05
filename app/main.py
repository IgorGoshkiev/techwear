import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select, text

from .database import Base, async_session, engine
from .models import Product
from .routers import products

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление событиями жизненного цикла приложения"""
    # Startup логика
    logger.info("Starting database initialization...")

    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Проверяем подключение к базе данных
    async with engine.connect() as test_conn:
        await test_conn.execute(text("SELECT 1"))
        logger.info("Подключение к базе данных успешно")

    # Создаем тестовые товары
    async with async_session() as session:
        try:
            # Проверяем, есть ли уже товары
            stmt = select(Product)
            result = await session.execute(stmt)
            existing_products = result.scalars().all()

            if existing_products:
                logger.info(f"В базе уже есть {len(existing_products)} товаров")
            else:
                # Создаем тестовые товары
                test_products = [
                    Product(
                        name="Waterproof Tech Jacket",
                        description="Техническая куртка с мембраной GORE-TEX",
                        price=299.99,
                        category="jackets",
                        sizes="S,M,L,XL"
                    ),
                    Product(
                        name="Cargo Tech Pants",
                        description="Функциональные штаны с карго-карманами",
                        price=199.99,
                        category="pants",
                        sizes="M,L,XL"
                    ),
                    Product(
                        name="Urban Backpack",
                        description="Городской рюкзак с водонепроницаемым отделением",
                        price=149.99,
                        category="accessories",
                        sizes="One Size"
                    )
                ]

                session.add_all(test_products)
                await session.commit()

                for product in test_products:
                    await session.refresh(product)

                logger.info(f"Создано {len(test_products)} тестовых товаров")

        except Exception as e:
            logger.error(f"Ошибка при создании тестовых данных: {str(e)}")
            # Не прерываем запуск при ошибке тестовых данных

    yield

    # Shutdown логика
    await engine.dispose()
    logger.info("Приложение завершает работу")


app = FastAPI(
    title="VNE Techwear Store API",
    description="Backend для интернет-магазина techwear бренда VNE",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(products.router,  tags=["Products"])


# Health check endpoint
@app.get("/health")
async def health_check():
    """Проверка статуса приложения"""
    return {
        "status": "healthy",
        "service": "VNE Techwear Store API",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    return {
        "message": "VNE Techwear Store API",
        "docs": "/docs",
        "health": "/health"
    }


# Глобальный обработчик ошибок
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(_request: Request, exc: HTTPException):
    error_detail = exc.detail

    if isinstance(error_detail, dict):
        error_content = error_detail
        logger.error(
            f"HTTPException: status_code={exc.status_code}, "
            f"error_type={exc.__class__.__name__}, "
            f"error_details={error_content}"
        )
    else:
        error_content = {
            "result": False,
            "error_type": exc.__class__.__name__,
            "error_message": str(error_detail),
        }
        logger.error(
            f"HTTPException: status_code={exc.status_code}, "
            f"error_type={exc.__class__.__name__}, "
            f"error_message={str(error_detail)}"
        )

    return JSONResponse(status_code=exc.status_code, content=error_content)


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "result": False,
            "error_type": "InternalServerError",
            "error_message": "Internal server error"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )