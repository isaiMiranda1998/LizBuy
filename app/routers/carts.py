from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.cart import CartItemRead, CartResponse, CartItemResponse, CartItemUpdate
from app.schemas.user import UserResponse
from app.core.exceptions import CartNotFoundError, ProductNotFoundError, InvalidProductQuantity, CartItemNotFoundError 
from app.services.cart_service import CartService
from app.dependencies.cart import get_cart_service
from app.dependencies.user import get_current_user
from typing import Annotated

router = APIRouter(
    prefix="/carts",
    tags=["Carts"]
)

@router.get("", response_model=CartResponse)
def get_cart_by_user_id(current_user: Annotated[UserResponse, Depends(get_current_user)], cart_service: Annotated[CartService, Depends(get_cart_service)]):
    try:
        return cart_service.get_cart_by_user_id(str(current_user.id))
    except CartNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))
    
@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def empty_cart(current_user: Annotated[UserResponse, Depends(get_current_user)], cart_service: Annotated[CartService, Depends(get_cart_service)]):
    try:
        cart_service.empty_cart(str(current_user.id))
    except (CartNotFoundError, CartItemNotFoundError) as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)) 

@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def create_cart_item(current_user: Annotated[UserResponse, Depends(get_current_user)], cart_item: CartItemRead, cart_service: Annotated[CartService, Depends(get_cart_service)]):
    try:
        return cart_service.create_cart_item(str(current_user.id), cart_item)
    except (CartNotFoundError, ProductNotFoundError) as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)) 
    except InvalidProductQuantity as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex)) 
    
@router.put("/items/{cart_item_id}", response_model=CartItemResponse)   
def update_cart_item(current_user: Annotated[UserResponse, Depends(get_current_user)], cart_item_id: str, cart_item_update: CartItemUpdate, cart_service: Annotated[CartService, Depends(get_cart_service)]):
    try:
        return cart_service.update_cart_item(str(current_user.id), cart_item_id, cart_item_update)
    except (CartNotFoundError, ProductNotFoundError) as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)) 