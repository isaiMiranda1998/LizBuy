from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class JwtSettings(BaseSettings):
    secret_key: str
    algorithm: Literal["HS256"] = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="JWT_",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class DbSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    name: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DB_",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class PaypalSettings(BaseSettings):
    api_key: str
    secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PAYPAL_",
        env_file_encoding="utf-8",
        extra="ignore"
    )

db_settings = DbSettings() #type: ignore
jwt_settings = JwtSettings() #type: ignore
paypal_settings = PaypalSettings() #type: ignore