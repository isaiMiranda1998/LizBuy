from pydantic import BaseModel, Field, ConfigDict, field_validator, field_serializer, model_validator
from decimal import Decimal, ROUND_HALF_UP
import uuid
from typing import Any, cast

class ProductRead(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)
    description: str | None = Field(default=None, min_length=5, max_length=1000)
    active: bool 

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: Decimal):
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

class ProductResponse(BaseModel):
    id: uuid.UUID
    name: str 
    price: Decimal 
    stock: int
    description: str | None
    active: bool 

    @field_serializer("id")
    def serialize_id(self, value: uuid.UUID):
        return str(value)

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

class ProductPartialUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    description: str | None = Field(default=None, min_length=5, max_length=1000)
    active: bool | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any):
        if not isinstance(data, dict):
            raise ValueError("Invalid input")
        
        data = cast(dict[str, Any], data)
        if not cls._has_at_least_one_value(data):
            raise ValueError("There must be at least one field to update")
        
        return data
    
    @classmethod
    def _has_at_least_one_value(cls, data: dict[str, Any]):
        return any(data.get(field) is not None for field in cls.model_fields)    

    model_config = ConfigDict(
        str_strip_whitespace=True
    )