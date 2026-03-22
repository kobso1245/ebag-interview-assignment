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
    description = fields.TextField() # set to text field, as generally the description could be quite a lot of text
    image = fields.CharField(max_length=1024) # TODO: Make better
    category = fields.ForeignKeyField(
        to='models.Category',
        related_name='parent'
    )

    def __str__(self):
        return self.title

    class Meta:
        table = "product"
        
    