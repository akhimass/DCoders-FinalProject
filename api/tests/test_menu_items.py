from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_menu_item():
    response = client.post("/menu_items", json={
        "name": "Ham Sandwich",
        "price": 7.99
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ham Sandwich"
    assert data["price"] == 7.99