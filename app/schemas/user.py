from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_serializer, model_validator
from typing import Any, cast
from datetime import datetime
import uuid

class UserRead(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(min_length=3, max_length=254)
    name: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=64)
    
    model_config = ConfigDict(
        str_strip_whitespace=True
    )

class UserResponse(BaseModel): 
    id: uuid.UUID
    username: str
    email: str
    name: str
    role: str
    created_at: datetime

    @field_serializer("id")
    def serialize_id(self, value: uuid.UUID):
        return str(value)

    model_config = ConfigDict(
        extra="ignore",
        from_attributes=True
    )

class UserPartialUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=20)
    email: EmailStr | None = Field(default=None, min_length=3, max_length=254)
    name: str | None  = Field(default=None, min_length=3, max_length=20)
    password: str | None  = Field(default=None, min_length=8, max_length=64)

    @model_validator(mode="before")
    @classmethod
    def check_at_least_one_field(cls, data: Any):
        if not isinstance(data, dict):
            raise ValueError("Invalid input")
        
        data = cast(dict[str, Any], data)
        if cls._has_at_least_one_value(data):
            return data
        
        raise ValueError("There must be at least one field to update")

    @classmethod
    def _has_at_least_one_value(cls, data: dict[str, Any]):
        return any(data.get(field) is not None for field in cls.model_fields)
