from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, Numeric, DateTime, Enum, ForeignKey
from app.db.base import Base
import uuid
from decimal import Decimal
from datetime import datetime
from .order import Currencies
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from .order import Order

class Providers(enum.Enum):
    PAYPAL = "PAYPAL"

class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELED = "CANCELED"

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), nullable=False, unique=True)
    provider: Mapped[enum.Enum] = mapped_column(Enum(Providers, name="providers_enum"), nullable=False)
    provider_payment_id: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    status: Mapped[enum.Enum] = mapped_column(Enum(PaymentStatus, name="payment_status_enum"), nullable=False, default=PaymentStatus.PENDING)
    amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    currency: Mapped[enum.Enum] = mapped_column(Enum(Currencies, name="currencies_enum"), nullable=False)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    order: Mapped["Order"] = relationship("Order", back_populates="payment")