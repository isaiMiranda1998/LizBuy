from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime
import uuid
from decimal import Decimal

class PayPalCheckoutResponse(BaseModel):
    payment_id: str
    approval_url: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

class PaymentResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    provider: str
    provider_payment_id: str
    status: str
    amount: Decimal
    currency: str
    paid_at: datetime

    @field_serializer("id", "order_id")
    def serialize_id(self, value: uuid.UUID):
        return str(value)
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )