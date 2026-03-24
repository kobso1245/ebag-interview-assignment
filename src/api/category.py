from fastapi import APIRouter, HTTPException
from tortoise.exceptions import ValidationError

from src.schemas.category import CategoryCreate, CategoryOut
from src.db.models import Category

router = APIRouter(prefix='/category')

@router.get("/")
async def get_categories() -> list[CategoryOut]:
    """
    Retrieve all the categories, that are available in the application.
    The response is ordered by id desc.
    Returns:
        list[CategoryOut]: _description_
    """
    return await Category.all().order_by('-category_id')

@router.get("/{item_id}/")
async def get_single_category(item_id: int) -> CategoryOut:
    return await Category.get(category_id=item_id)

@router.put('/{item_id}/')
async def update_single_category(item_id: int, category: CategoryCreate):
    if not await Category.filter(category_id=item_id).exists():
        return HTTPException(status_code=404, detail=f'Category with id {item_id} not found!')

    try:
        await Category.filter(category_id=item_id).update(name=category.name)    
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/", status_code=201)
async def create_category(category: CategoryCreate):
    """
    Create a new Category object.
    If category with the provided name exists - an error response is returned.

    Args:
        category (CategoryCreate): _description_

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    if await Category.filter(name=category.name).exists():
       return HTTPException(status_code=404, detail=f'Category with the given name exists!')

    try:
        return await Category.create(name=category.name)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.delete("/{item_id}/")
async def delete_category(item_id: int):
    """
    Delete a Category object with provided id. If the object does not exist - error is not raised.
    
    Args:
        item_id (int): _description_

    Returns:
        _type_: _description_
    """
    return await Category.get(category_id=item_id).delete()