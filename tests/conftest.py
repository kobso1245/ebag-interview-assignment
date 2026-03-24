import os
import sys
import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src.main import app
from src.db.models import Category, Product

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with LifespanManager(app):
        async with AsyncClient(
            transport=transport,
            base_url="http://test"
        ) as ac:
            yield ac
