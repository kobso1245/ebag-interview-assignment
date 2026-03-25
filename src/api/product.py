from datetime import datetime
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import ValidationError

from src.schemas.product import ProductOut, ProductCreate, ProductUpdate
from src.utils.conf import read_config
from src.db.models import Product, Category

router = APIRouter(prefix='/product')
config = read_config()

@router.get("/search/")
async def search(
    title: str | None = None,
    description: str | None = None,
    min_price: str | None = None,
    max_price: str | None = None,
    added_before: datetime | None = None,
    added_after: datetime | None = None
) -> list[ProductOut]:
    """
    Return list of products, based on the provided properties, passed as query params.
    """
    return await Product.custom_filter(
        title=title,
        description=description,
        min_price=min_price,
        max_price=max_price,
        added_before=added_before,
        added_after=added_after
    )

@router.get("/")
async def get_all_products() -> list[ProductOut]:
    """
    Return a list of all Products, available in the DB.
    The order is based on updated_at desc.
    """
    data = await Product.all().prefetch_related('category').order_by('-updated_at')
    return data

@router.get("/{item_id}/")
async def get_single_product(item_id: str) -> ProductOut:
    """
    Return a list of all Products, available in the DB.
    The order is based on updated_at desc.
    """
    data = await Product.get(unique_product_id=item_id).prefetch_related('category')
    return data

@router.post("/", response_model=ProductOut, status_code=201)
async def create_product(data: ProductCreate = Depends()):
    """
    Create a new Product object, with the provided properties, and return it.
    """
    # perform validation
    category_exists = await Category.filter(category_id=data.category_id).exists()
    if not category_exists:
        raise HTTPException(status_code=400, detail="The provided category does not exist!")
    title_exists = await Product.filter(title=data.title).exists()
    if title_exists:
        raise HTTPException(status_code=400, detail="Product with same title exists!")
    
    # Generate unique filename
    file_path = None
    if data.image:
        file_ext = data.image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(config.get('general', 'files_dir'), filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await data.image.read())

    # Save to DB
    try:
        item = await Product.create(image_path=file_path, **data.for_save())
        await item.refresh_from_db()
        await item.fetch_related('category')
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return item

@router.put('/{item_id}/')
async def update_single_product(item_id: str, product: ProductUpdate = Depends()):
    if not await Product.filter(unique_product_id=item_id).exists():
        return HTTPException(status_code=404, detail=f'Product with id {item_id} not found!')

    try:
        await Product.filter(unique_product_id=item_id).update(**product.updated())    
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    
    return await Product.get(unique_product_id=item_id)

@router.delete("/{item_id}/")
async def delete_product(item_id: str):
    """
    Delete a Product by given object id
    """
    await Product.get(unique_product_id=item_id).delete()