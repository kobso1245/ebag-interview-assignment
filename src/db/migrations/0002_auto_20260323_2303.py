from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_initial')]

    initial = False

    operations = [
        ops.RenameField(
            model_name='Product',
            old_name='image',
            new_name='image_path',
        ),
        ops.AddField(
            model_name='Product',
            name='created_at',
            field=fields.DatetimeField(auto_now=False, auto_now_add=True),
        ),
        ops.AddField(
            model_name='Product',
            name='price',
            field=fields.FloatField(),
        ),
        ops.AddField(
            model_name='Product',
            name='updated_at',
            field=fields.DatetimeField(auto_now=True, auto_now_add=False),
        ),
    ]
