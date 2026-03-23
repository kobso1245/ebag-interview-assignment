from pydantic import BaseModel, UUID4

from category import CategoryOut

class ProductCreate(BaseModel):
    title: str
    description: str
    image: str
    category_id: int # pass the category_id to backend

class ProductOut(BaseModel):
    unique_product_id: UUID4
    title: str
    description: str
    image: bytes
    category: CategoryOut