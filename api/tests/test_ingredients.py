from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_ingredient():
    response = client.post("/ingredients", json={
        "name": "Lettuce",
        "quantity": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Lettuce"
    assert data["quantity"] == 10