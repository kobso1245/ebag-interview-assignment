from tortoise import fields
from tortoise.models import Model

class Category(Model):
    category_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256)
    
    class Meta:
        table = 'category'

class Product(Model):
    unique_product_id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=256)
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

    def __str__(self):
        return self.title

    class Meta:
        table = "product"
        
    