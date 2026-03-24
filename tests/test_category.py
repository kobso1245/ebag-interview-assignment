import pytest

from src.db.models import Category

@pytest.mark.asyncio
async def test_list_items(client):
    await Category.create(name='Test category')
    
    response = await client.get(
        "/api/category/"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["name"] == "Test category"
    
    # cleanup the entries written
    await Category.all().delete()
    

@pytest.mark.asyncio
async def test_create_item(client):
    response = await client.post(
        "/api/category/",
        json={"name": "Zarzavat3"}
    )

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Zarzavat3"
    
    response = await client.get(
        "/api/category/"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["name"] == "Zarzavat3"
    
    # cleanup the entries written
    await Category.all().delete()
    
@pytest.mark.asyncio
async def test_delete_item(client):
    category = await Category.create(name='Zarzavat')
    
    response = await client.delete(
        f"/api/category/{category.category_id}/"
    )

    assert response.status_code == 200
    
    response = await client.get(
        "/api/category/"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
    
    # cleanup the entries written
    await Category.all().delete()
    
@pytest.mark.asyncio
async def test_update_item(client):
    category = await Category.create(name='Zarzavat')
    
    response = await client.put(
        f"/api/category/{category.category_id}/",
        json={"name": "chushki"}
    )
    assert response.status_code == 200
    

    category = await Category.get(category_id=category.category_id)    
    assert category.name == 'chushki'
    
    # test field too long
    response = await client.put(
        f"/api/category/{category.category_id}/",
        json={"name": 257 * 'a'}
    )
    assert response.status_code == 400
    
    # cleanup the entries written
    await Category.all().delete()