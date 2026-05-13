from pydantic import BaseModel, Field, field_validator, ConfigDict, field_serializer
from decimal import Decimal
from datetime import datetime
import uuid

class OrderCreate(BaseModel):
    currency: str | None = Field(default=None)
    shipping_adress: str = Field(min_length=8, max_length=255)

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    @field_validator("currency")
    @classmethod
    def upper(cls, value: str):
        return value.upper()
    
class OrderResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    status: str
    total_amount: Decimal
    currency: str
    shipping_address: str
    created_at: datetime
    updated_at: datetime | None
    order_items: list[OrderItemResponse]

    @field_serializer("id", "user_id")
    def serialize_id(self, value: uuid.UUID):
        return str(value)

    model_config = ConfigDict(
        from_attributes=True
    )
    
class OrderItemResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    @field_serializer("id", "order_id", "product_id")
    def serialize_id(self, value: uuid.UUID):
        return str(value)

    model_config = ConfigDict(
        from_attributes=True
    )