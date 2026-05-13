from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductRead, ProductResponse, ProductPartialUpdate
from app.core.exceptions import ProductNotFoundError
from app.models.product import Product
from .helpers import parse_id, generate_uuid4

class ProductService:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo
    
    def get_product_by_id(self, product_id: str):
        return ProductResponse.model_validate(self._get_product_by_id(product_id))
    
    def get_products(self):
        products = self.repo.get_products()
        return [ProductResponse.model_validate(product) for product in products]
    
    def create_product(self, product: ProductRead):
        product_db = Product(
            id = generate_uuid4(),
            name = product.name,
            price = product.price,
            stock = product.stock,
            description = product.description,
            active = product.active
        )

        return ProductResponse.model_validate(self.repo.create_product(product_db))
    
    def update_product(self, product_id: str, product_update: ProductRead):
        product = self._get_product_by_id(product_id)
        
        updated_product = self.repo.update_product(product, **product_update.model_dump())
        
        return ProductResponse.model_validate(updated_product)
    
    def partial_update_product(self, product_id: str, product_update: ProductPartialUpdate):
        return ProductResponse.model_validate(
            self.repo.partial_update_product(
                self._get_product_by_id(product_id), 
                **product_update.model_dump()
            )
        )

    def decrease_stock_product(self, product_id: str, quantity: int):
        product = self._get_product_by_id(product_id)
        new_stock = product.stock - quantity
        
        return ProductResponse.model_validate(
            self.repo.partial_update_product(
                product, 
                stock = new_stock
            )
        )
        
    def _get_product_by_id(self, product_id: str):
        product = self.repo.get_product_by_id(parse_id(product_id))
        
        if not product:
            raise ProductNotFoundError(f"Product with id {product_id} doesn't exist")
        
        return product
    
    def delete_product(self, product_id: str):
        product = self.repo.get_product_by_id(parse_id(product_id))
        
        if not product:
            raise ProductNotFoundError(f"Product with id {product_id} doesn't exist")
        
        self.repo.delete_product(product)
