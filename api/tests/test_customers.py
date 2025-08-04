from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_customer():
    response = client.post("/customers", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"