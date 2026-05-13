from pydantic import BaseModel, ConfigDict, Field, field_validator

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=64)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        return value.lower()

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
        from_attributes=True
    )   

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class RefreshToquenRequest(BaseModel):
    refresh_token: str
