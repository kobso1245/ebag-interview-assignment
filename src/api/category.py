from fastapi import APIRouter
from schemas.category import CategoryCreate, CategoryOut

# TODO: move to services
from db.models import Category

router = APIRouter(prefix='/category')

@router.get("/")
async def get_categories() -> list[CategoryOut]:
    return await Category.all()

@router.get("/{item_id}")
async def get_single_category(item_id: int) -> CategoryOut:
    return await Category.get(category_id=item_id)

@router.put('/{item_id}')
async def update_single_category(item_id: int, category: CategoryCreate):
    return

@router.post("/", status_code=201)
async def create_category(category: CategoryCreate):
    return await Category.create(name=category.name)

@router.delete("/{item_id}")
async def delete_category(item_id: int):
    return await Category.get(category_id=item_id).delete()