from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200), 
        nullable=False
        )
    description: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True
        )
    
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), 
        nullable=False
        )

    stock: Mapped[int] = mapped_column(
        default=0,
        nullable=False
        )
    
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), 
        nullable=False
        )