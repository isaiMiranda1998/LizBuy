from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.exceptions import InvalidToken, UserNotFoundError
from app.core.security import verify_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.cart_repository import CartRepository
from app.dependencies.cart import get_cart_repository
from app.services.user_service import UserService
from typing import Annotated, Any

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/refresh")

def get_user_repository(db: Annotated[Session, Depends(get_db)]):
    return UserRepository(db)

def get_user_service(user_repository: Annotated[UserRepository, Depends(get_user_repository)], cart_repository: Annotated[CartRepository, Depends(get_cart_repository)]):
    return UserService(user_repository, cart_repository)

def require_auth(access_token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        return verify_token(access_token)
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

def get_current_user(payload: Annotated[dict[str, Any], Depends(require_auth)], user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        user_id = payload["sub"]
        return user_service.get_user(user_id)
    except UserNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))