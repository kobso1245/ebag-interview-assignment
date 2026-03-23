from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Category',
            fields=[
                ('category_id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('name', fields.CharField(unique=True, max_length=256)),
            ],
            options={'table': 'category', 'app': 'models', 'pk_attr': 'category_id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Product',
            fields=[
                ('unique_product_id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('title', fields.CharField(unique=True, max_length=256)),
                ('description', fields.TextField(unique=False)),
                ('image_path', fields.CharField(max_length=1024)),
                ('price', fields.FloatField()),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
                ('category', fields.ForeignKeyField('models.Category', source_field='category_id', db_constraint=True, to_field='category_id', related_name='parent', on_delete=OnDelete.CASCADE)),
            ],
            options={'table': 'product', 'app': 'models', 'pk_attr': 'unique_product_id'},
            bases=['Model'],
        ),
    ]
