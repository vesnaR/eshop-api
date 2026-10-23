
from decimal import Decimal


def test_create_product_with_existing_category(client):
    # Create a category first
    category_response = client.post(
        "/categories/",
        json={
            "name": "Test Electronics",
            "description": "Category for automated tests",
        },
    )

    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    # Create a product in that category
    product_response = client.post(
        "/products/",
        json={
            "name": "Test Laptop",
            "description": "Product created by pytest",
            "price": "899.99",
            "stock": 5,
            "category_id": category_id,
        },
    )

    assert product_response.status_code == 201

    product = product_response.json()
    assert product["name"] == "Test Laptop"
    assert Decimal(str(product["price"])) == Decimal("899.99")
    assert product["category_id"] == category_id


def test_create_product_with_nonexistent_category(client):
    response = client.post(
        "/products/",
        json={
            "name": "Invalid Product",
            "price": "19.99",
            "stock": 1,
            "category_id": 999999,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."



def test_update_product_successfully(client):
    category_response = client.post(
        "/categories/",
        json={
            "name": "Update Test Category",
            "description": "Category for update tests",
        },
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Original Product",
            "price": "50.00",
            "stock": 3,
            "category_id": category_id,
        },
    )
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Product",
            "price": "75.50",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"
    assert response.json()["price"] == "75.50"
    assert response.json()["stock"] == 3
    assert response.json()["category_id"] == category_id


def test_update_nonexistent_product(client):
    response = client.put(
        "/products/999999",
        json={"name": "Updated Product"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."


def test_update_product_with_nonexistent_category(client):
    category_response = client.post(
        "/categories/",
        json={"name": "Category For Invalid Update"},
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Product For Invalid Update",
            "price": "20.00",
            "category_id": category_id,
        },
    )
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={"category_id": 999999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."


def test_delete_product_successfully(client):
    category_response = client.post(
        "/categories/",
        json={"name": "Delete Test Category"},
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Product To Delete",
            "price": "25.00",
            "category_id": category_id,
        },
    )
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_product(client):
    response = client.delete("/products/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."


def test_create_product_rejects_short_name(client):
    category_response = client.post(
        "/categories/",
        json={"name": "Validation Category"},
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    response = client.post(
        "/products/",
        json={
            "name": "A",
            "price": "10.00",
            "category_id": category_id,
        },
    )

    assert response.status_code == 422


def test_create_product_rejects_zero_price(client):
    category_response = client.post(
        "/categories/",
        json={"name": "Price Validation Category"},
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    response = client.post(
        "/products/",
        json={
            "name": "Valid Product",
            "price": "0",
            "category_id": category_id,
        },
    )

    assert response.status_code == 422


def test_create_product_rejects_negative_stock(client):
    category_response = client.post(
        "/categories/",
        json={"name": "Stock Validation Category"},
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    response = client.post(
        "/products/",
        json={
            "name": "Valid Product",
            "price": "10.00",
            "stock": -1,
            "category_id": category_id,
        },
    )

    assert response.status_code == 422
