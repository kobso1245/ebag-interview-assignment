from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os

from src.api import category, product
from src.utils.conf import build_db_config

# Register FastAPI main app
app = FastAPI(title="Ebag Interview Assignment")

register_tortoise(
    app,
    config=build_db_config(),
    add_exception_handlers=True,
    # generate the config when in test mode
    generate_schemas=os.environ.get('ENV', 'LOCAL') == 'TEST'
)

# add the different routes
app.include_router(category.router, prefix='/api')
app.include_router(product.router, prefix='/api')
