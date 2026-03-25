from datetime import datetime
from fastapi import Form, UploadFile, File
from pydantic import BaseModel, UUID4
from typing import Optional

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
        image: Optional[UploadFile] = File(None)
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
        
class ProductUpdate():
    def __init__(
        self,
        # pass the product properties as form fields
        title: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        price: Optional[float] = Form(None),
        category_id: Optional[int] = Form(None),
        # pass the file as file object
        image: Optional[UploadFile] = File(None)
    ):
        self.title = title
        self.description = description
        self.price = price
        self.category_id = category_id
        self.image = image
        
    def updated(self):
        props = {}
        if self.title is not None:
            props['title'] = self.title
        if self.description is not None:
            props['description'] = self.description
        if self.price is not None:
            props['price'] = self.price
        if self.category_id is not None:
            props['category_id'] = self.category_id
        if self.image is not None:
            props['image'] = self.image
            
        return props
            

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