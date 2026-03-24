from datetime import datetime
from fastapi import Form, UploadFile, File
from pydantic import BaseModel, UUID4

from src.api.category import CategoryOut

class ProductCreate:
    def __init__(
        self,
        # pass the product properties as form fields
        title: str = Form(...),
        description: str = Form(),
        price: float = Form(),
        category_id: int = Form(),
        # pass the file as file object
        image: UploadFile = File(...)
    ):
        self.title = title
        self.description = description
        self.price = price
        self.category_id = category_id
        self.image = image
        
    def for_save(self):
        return {
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "category_id": self.category_id
        }

class ProductOut(BaseModel):
    unique_product_id: UUID4
    title: str
    description: str | None
    image_path: str | None
    category: CategoryOut
    #category_id: int
    price: float
    created_at: datetime
    updated_at: datetime