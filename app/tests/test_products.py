
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
