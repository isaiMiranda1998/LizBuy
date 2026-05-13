from pydantic import BaseModel, field_serializer, ConfigDict, Field, field_validator
from datetime import datetime
from decimal import Decimal
from typing import Any
import uuid

class CartRead(BaseModel):
    user_id: str

class CartResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None
    cart_items: list[CartItemResponse]

    @field_serializer("id", "user_id")
    def serialize_uuid(self, value: uuid.UUID):
        return str(value)
    
    @field_validator("cart_items", mode="before")
    @classmethod
    def serialize_cart_items(cls, values: Any) -> list[CartItemResponse]:
        if values is None:
            return []
        
        return [CartItemResponse.model_validate(item) for item in values]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )
    
class CartItemRead(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)
    
class CartItemResponse(BaseModel):
    id: uuid.UUID
    cart_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal
    created_at: datetime
    updated_at: datetime | None

    @field_serializer("id", "cart_id", "product_id")
    def serialize_uuid(self, value: uuid.UUID):
        return str(value)
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )