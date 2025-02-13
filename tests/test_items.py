import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_items():
    response = client.get("/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item():
    response = client.post("/v1/items/", json={
        "name": "Item Test",
        "description": "Descrição",
        "price": 9.99
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Item Test"
    assert data["price"] == 9.99
