from datetime import datetime
import os
import uuid
from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from src.schemas.product import ProductOut, ProductCreate
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
    # Filter and Search for Product
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
    data = await Product.all().prefetch_related('category').order_by('-updated_at')
    return data

@router.get("/{item_id}/")
async def get_single_product(item_id: str) -> ProductOut:
    data = await Product.get(unique_product_id=item_id).prefetch_related('category')
    return data

@router.post("/", response_model=ProductOut)
async def create_product(data: ProductCreate = Depends()):
    # perform validation
    category_exists = await Category.filter(category_id=data.category_id).exists()
    if not category_exists:
        raise HTTPException(status_code=400, detail="The provided category does not exist!")
    title_exists = await Product.filter(title=data.title).exists()
    if title_exists:
        raise HTTPException(status_code=400, detail="Product with same title exists!")
    
    # Generate unique filename
    file_ext = data.image.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(config.get('general', 'files_dir'), filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(await data.image.read())

    # Save to DB
    try:
        item = await Product.create(image_path=file_path, **data.for_save())
        item.refresh_from_db()
        await item.fetch_related('category')
    except Exception as exc:
        print(type(exc))
        return

    return item

@router.delete("/{item_id}/")
async def delete_product(item_id: str):
    await Product.get(unique_product_id=item_id).delete()