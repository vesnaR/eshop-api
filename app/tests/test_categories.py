
def test_create_category_successfully(client):
    response = client.post(
        "/categories/",
        json={
            "name": "Books",
            "description": "Books and publications",
        },
    )

    assert response.status_code == 201

    category = response.json()
    assert category["name"] == "Books"
    assert category["description"] == "Books and publications"
    assert "id" in category


def test_create_duplicate_category_returns_409(client):
    category_data = {
        "name": "Unique Category",
        "description": "Test duplicate handling",
    }

    first_response = client.post("/categories/", json=category_data)
    assert first_response.status_code == 201

    second_response = client.post("/categories/", json=category_data)

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "A category with this name already exists."
    )


def test_get_categories_returns_created_category(client):
    create_response = client.post(
        "/categories/",
        json={
            "name": "Office Supplies",
            "description": "Office products",
        },
    )
    assert create_response.status_code == 201

    response = client.get("/categories/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Office Supplies"
    assert response.json()[0]["products"] == []


def test_create_category_rejects_empty_name(client):
    response = client.post(
        "/categories/",
        json={"name": ""},
    )

    assert response.status_code == 422

