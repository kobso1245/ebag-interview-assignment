from fastapi import FastAPI
import json
from tortoise.contrib.fastapi import register_tortoise

from api import category, product

# Register FastAPI main app
app = FastAPI(title="Ebag Interview Assignment")

with open("confs/db.json") as f:
    tortoise_config = json.load(f)

register_tortoise(
    app,
    config=tortoise_config,
    add_exception_handlers=True,
)

# add the different routes
app.include_router(category.router, prefix='/api')
app.include_router(product.router, prefix='/api')
