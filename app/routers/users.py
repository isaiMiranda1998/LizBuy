from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.user import get_current_user, get_user_service
from app.services.user_service import UserService
from app.schemas.user import UserPartialUpdate, UserResponse, UserRead
from app.core.exceptions import UserNotFoundError
from typing import Annotated

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.patch("", response_model=UserResponse)
def partial_update_user(current_user: Annotated[UserResponse, Depends(get_current_user)], user_update: UserPartialUpdate, user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        return user_service.partial_update_user(str(current_user.id), user_update) 
    except UserNotFoundError as ex:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(ex))
    
@router.put("", response_model=UserResponse)
def update_user(current_user: Annotated[UserResponse, Depends(get_current_user)], user_update: UserRead, user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        return user_service.update_user(str(current_user.id), user_update) 
    except UserNotFoundError as ex:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(ex))
    
@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: Annotated[UserResponse, Depends(get_current_user)], user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        user_service.delete_user(str(current_user.id)) 
    except UserNotFoundError as ex:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(ex))