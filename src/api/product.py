from fastapi import APIRouter
from schemas.category import CategoryCreate

# TODO: move to services
from db.models import Category

router = APIRouter()

@router.get("/product")
async def get_products():
    return await Category.all()

@router.post("/product")
async def create_product(category: CategoryCreate):
    return await Category.create(name=category.name)