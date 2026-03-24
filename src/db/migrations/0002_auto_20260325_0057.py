from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_initial')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='Product',
            name='description',
            field=fields.TextField(null=True, unique=False),
        ),
        ops.AlterField(
            model_name='Product',
            name='image_path',
            field=fields.CharField(null=True, max_length=1024),
        ),
    ]
