from datetime import datetime
from tortoise import fields
from tortoise.models import Model
from tortoise.expressions import Q

class Category(Model):
    category_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256, unique=True)
    
    class Meta:
        table = 'category'

class Product(Model):
    unique_product_id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=256, unique=True)
    # set to text field, as generally the description could be quite a lot of text
    description = fields.TextField()
    # the images will be stored on the local filesystem and the path will be stored in the DB
    # with a randomly generated name of the image
    image_path = fields.CharField(max_length=1024)
    price = fields.FloatField()
    # keep the initial datetime when the product was created
    created_at = fields.DatetimeField(auto_now_add=True)
    # keep the last update of the product
    updated_at = fields.DatetimeField(auto_now=True)
    category = fields.ForeignKeyField(
        to='models.Category',
        related_name='parent'
    )

    @classmethod
    async def custom_filter(
        cls: Product,
        title: str | None,
        description: str | None,
        min_price: str | None,
        max_price: str | None,
        added_before: datetime | None,
        added_after: datetime | None
    ):
        query = Q()
        
        if title:
            query &= Q(title__icontains=title)

        if description:
            query &= Q(description__icontains=description)

        if min_price is not None:
            query &= Q(price__gte=min_price)

        if max_price is not None:
            query &= Q(price__lte=max_price)
        
        if added_before is not None:
            query &= Q(created_at__lte=added_before)
        
        if added_after is not None:
            query &= Q(created_at__gte=added_after)

        return await cls.filter(query).prefetch_related('category').order_by('-created_at')

    def __str__(self):
        return self.title
    
    def build_unique_name(self):
        return f''


    class Meta:
        table = "product"
        
    