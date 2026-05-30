import uuid

def parse_id(product_id: str):
    try:
        return uuid.UUID(product_id)
    except ValueError:
        raise ValueError(f"Invalid UUID format: {product_id}")
        
def generate_uuid4():
    return uuid.uuid4()