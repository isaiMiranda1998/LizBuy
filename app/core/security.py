from datetime import datetime, timezone, timedelta
from app.core.config import jwt_settings
from typing import TypeAlias
import jwt
from typing import Any
import bcrypt
from app.core.exceptions import InvalidToken

JWTCLAIMS: TypeAlias = dict[str, Any]

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("ascii")

def verify_password(password: str, hashed_password: str): 
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_access_token(payload: JWTCLAIMS, expires_delta: timedelta | None = None):
    to_encode = payload.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=jwt_settings.access_token_expire_minutes))
    issued_at = datetime.now(timezone.utc)

    to_encode.update({"exp": expire})
    to_encode.update({"iat": issued_at})

    return jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)

def create_refresh_token(payload: JWTCLAIMS, expires_delta: timedelta | None = None):
    to_encode = payload.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=jwt_settings.refresh_token_expire_days))
    issued_at = datetime.now(timezone.utc)

    to_encode.update({"exp": expire})
    to_encode.update({"iat": issued_at})

    return (jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm), expire)

def verify_token(token: str):
    try:
        return jwt.decode(token, jwt_settings.secret_key, jwt_settings.algorithm) 
    except jwt.InvalidTokenError:
        raise InvalidToken("Invalid refresh token")
    