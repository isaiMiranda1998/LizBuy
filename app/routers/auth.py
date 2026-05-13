from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import LoginRequest, TokenResponse, RefreshToquenRequest
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from typing import Annotated
from app.core.exceptions import InvalidToken
from app.dependencies.auth import get_auth_service
from app.dependencies.user import get_user_service
from app.core.exceptions import InvalidCredentials
from app.schemas.user import UserRead, UserResponse
from app.core.exceptions import EmailExists, UsernameExists

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=TokenResponse)
def login(user_data: LoginRequest, service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        return service.login_user(user_data)
    except InvalidCredentials as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_token: RefreshToquenRequest, service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        return service.refresh_access_token(refresh_token.refresh_token)
    except InvalidToken as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) 
    
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserRead, user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        return user_service.create_user(user_data)
    except (EmailExists, UsernameExists) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) 