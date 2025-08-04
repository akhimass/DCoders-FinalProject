from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_review():
    response = client.post("/reviews", json={
        "rating": 5,
        "comment": "Excellent!",
        "customer_name": "Bob"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Excellent!"