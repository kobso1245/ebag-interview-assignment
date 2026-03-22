from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str

class CategoryOut(BaseModel):
    category_id: int
    name: str