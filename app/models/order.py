from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid, func, DateTime, Enum, ForeignKey, Numeric, String, Integer
from app.db.base import Base
from datetime import datetime
import uuid
import enum
from decimal import Decimal
from typing import TYPE_CHECKING
from .user import User


if TYPE_CHECKING:
    from .user import User
    from .payment import Payment

class Currencies(enum.Enum):
    CRC = "CRC"
    USD = "USD"

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
                  
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False) 
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status_enum"), nullable=False, default=OrderStatus.PENDING)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False) 
    currency: Mapped[Currencies] = mapped_column(Enum(Currencies, name="currencies_enum"), nullable=False, default=Currencies.CRC)
    shipping_address: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
    user: Mapped["User"] = relationship("User", back_populates="orders")
    payment: Mapped["Payment"] = relationship("Payment", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), nullable=False) 
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), nullable=False) 
    product_name: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False) 
    total_price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False) 
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
