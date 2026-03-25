import pytest

from src.db.models import Category, Product

async def cleanup():
    # cleanup the DB entries written
    await Category.all().delete()
    await Product.all().delete()

@pytest.mark.asyncio
async def test_list_items(client):
    """Verify that the general listing of products behaves as expected"""
    category = await Category.create(name='Test category')
    product = await Product.create(
        title='Product 1',
        description='Dummy Product for testing',
        price=1.5,
        category=category
    )
    
    response = await client.get(
        "/api/product/"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["title"] == "Product 1"
    assert data[0]["description"] == "Dummy Product for testing"
    assert data[0]['price'] == 1.5
    
    # cleanup the entries written
    await cleanup()
    

@pytest.mark.asyncio
async def test_create_item(client):
    """Verify that the Product creation endpoint works as expected"""
    category = await Category.create(name='Test category')
    response = await client.post(
        "/api/product/",
        data={
            "title": "Dummy Product",
            "description": "Dummy product description",
            "category_id": category.category_id,
            "price": 1.5
        }
    )
    
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Dummy Product"
    assert data["description"] == "Dummy product description"
    # the whole category object is returned
    assert data["category"]["name"] == 'Test category'
    assert data["category"]["category_id"] == category.category_id
    
    # cleanup the entries written
    await cleanup()
    
@pytest.mark.asyncio
async def test_update_item(client):
    category = await Category.create(name='Test category')
    product = await Product.create(
        title='Product 1',
        description='Dummy Product for testing',
        price=1.5,
        category=category
    )
    
    response = await client.put(
        f"/api/product/{product.unique_product_id}/",
        data={
            "title": "Updated product",
            "price": 2.5
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Updated product"
    assert data['price'] == 2.5
    assert data['description'] == 'Dummy Product for testing'
    
    # cleanup the entries written
    await cleanup()
    
@pytest.mark.asyncio
async def test_search(client):
    category = await Category.create(name='Test category')
    product_1 =await Product.create(
        title='Dummy 0 Product',
        description='Dummy Product for testing',
        price=1.5,
        category=category
    )
    
    product_2 = await Product.create(
        title='Dummy 1 Product',
        description='Dummy Product for testing',
        price=3,
        category=category
    )
    
    response = await client.get(
        f"/api/product/search/"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    search_params = {'title': 'Dummy 1'}
    response = await client.get(
        f"/api/product/search/",
        params=search_params
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['unique_product_id'] == str(product_2.unique_product_id)
    
    search_params = {'title': 'Dummy 1', 'min_price': 2}
    response = await client.get(
        f"/api/product/search/",
        params=search_params
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['unique_product_id'] == str(product_2.unique_product_id)
    
    
    search_params = {'max_price': 2}
    response = await client.get(
        f"/api/product/search/",
        params=search_params
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['unique_product_id'] == str(product_1.unique_product_id)
    
    await cleanup()    


@pytest.mark.asyncio
async def test_delete_item(client):
    """Verify that an existing product can be deleted from the DB"""
    category = await Category.create(name='Test category')
    product = await Product.create(
        title='Product 1',
        description='Dummy Product for testing',
        price=1.5,
        category=category
    )
    
    response = await client.delete(
        f"/api/product/{product.unique_product_id}/"
    )
    
    assert response.status_code == 200
    
    assert await Product.all().count() == 0
    
    # cleanup the entries written
    await cleanup()