from typing import TYPE_CHECKING
from sqlalchemy import String, Enum, DateTime, func, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime
import enum
import uuid

if TYPE_CHECKING:
    from .auth import RefreshToken
    from .cart import Cart
    from .order import Order

class Roles(enum.Enum):
    USER = "user"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[Roles] = mapped_column(
        Enum(Roles, name="roles_enum"), 
        nullable=False, 
        default=Roles.USER
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, server_default=func.now()
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship("RefreshToken", back_populates="user")
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")

