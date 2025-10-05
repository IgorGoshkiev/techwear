from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from .database import Base


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Название товара"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Описание товара"
    )
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Цена товара"
    )
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="Категория товара"
    )
    sizes: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Доступные размеры (через запятую)"
    )