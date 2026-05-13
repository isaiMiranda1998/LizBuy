from fastapi import APIRouter, Depends, HTTPException, status
from app.services.order_service import OrderService
from app.schemas.order import OrderResponse, OrderCreate
from app.schemas.user import UserResponse
from app.core.exceptions import InvalidProductQuantity, CartNotFoundError, InvalidCurrency, OrderNotFoundError
from app.dependencies.order import get_order_service
from app.dependencies.user import require_auth, get_current_user
from typing import Annotated

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/{order_id}", response_model=OrderResponse, dependencies=[Depends(require_auth)])
def get_order_by_id(order_id: str, order_service: Annotated[OrderService, Depends(get_order_service)]):
    try:
        return order_service.get_order(order_id)
    except OrderNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)) 
    
@router.post("/checkout", response_model=OrderResponse)
def create_order(current_user: Annotated[UserResponse, Depends(get_current_user)],order_data: OrderCreate, order_service: Annotated[OrderService, Depends(get_order_service)]):
    try:
        return order_service.create_order(str(current_user.id), order_data)
    except (InvalidProductQuantity, InvalidCurrency) as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    except CartNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)) 