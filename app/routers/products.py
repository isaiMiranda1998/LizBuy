from fastapi import APIRouter, Depends, status, HTTPException
from app.core.exceptions import ProductNotFoundError
from app.schemas.product import ProductResponse, ProductRead
from app.services.product_service import ProductService
from app.dependencies.product import get_product_service
from typing import Annotated
from app.dependencies.user import require_auth

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("", response_model=list[ProductResponse])
def get_products(product_service: Annotated[ProductService, Depends(get_product_service)]):
    return product_service.get_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: str, product_service: Annotated[ProductService, Depends(get_product_service)]):
    try:
        return product_service.get_product_by_id(product_id)
    except ProductNotFoundError as ex:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(ex))
    except ValueError as ex:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(ex))

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_auth)])
def create_product(product: ProductRead, product_service: Annotated[ProductService, Depends(get_product_service)]):
    return product_service.create_product(product)

@router.put("/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_auth)])
def update_product(product_id: str, product_update: ProductRead, product_service: Annotated[ProductService, Depends(get_product_service)]):
    try:
        return product_service.update_product(product_id, product_update)
    except ProductNotFoundError as ex:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(ex))
    except ValueError as ex:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(ex))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_auth)])
def delete_product(product_id: str, product_service: Annotated[ProductService, Depends(get_product_service)]):
    try:
        product_service.delete_product(product_id)
    except ProductNotFoundError as ex:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(ex))
    except ValueError as ex:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(ex))