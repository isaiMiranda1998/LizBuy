from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid, Boolean, String, Integer, Numeric
from app.db.base import Base
import uuid
from decimal import Decimal

class Product(Base):
    __tablename__ = "products"
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)