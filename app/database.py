from datetime import datetime
from typing import Annotated, Any, AsyncGenerator, List, Optional

from sqlalchemy import ARRAY, Integer, String, func, text
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from config_db import settings

DATABASE_URL = settings.get_db_url()

print("DB URL =>", settings.get_db_url())
print("DB HOST =>", settings.DB_HOST)

# Создаёт асинхронное подключение к базе данных PostgreSQL, используя драйвер asyncpg.
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаёт фабрику асинхронных сессий, используя созданный движок.
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


# Аннотации для колонок
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
array_or_none_an = Annotated[Optional[List[str]], mapped_column(ARRAY(String(255)))]


# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Уникальный идентификатор записи",
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), comment="Дата и время создания записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        comment="Дата и время последнего обновления записи",
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"