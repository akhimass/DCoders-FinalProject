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

def test_delete_review():
    customer_resp = client.post("/customers/", json={
        "name": "Test Customer",
        "email": "testcustomer@example.com"
    })
    assert customer_resp.status_code == 200
    customer_id = customer_resp.json()["id"]

    review_resp = client.post("/reviews/", json={
        "rating": 4,
        "comment": "Good test review",
        "customer_id": customer_id
    })
    assert review_resp.status_code == 200
    review_id = review_resp.json()["id"]

    delete_resp = client.delete(f"/reviews/{review_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"detail": "Review deleted"}

    get_resp = client.get(f"/reviews/{review_id}")
    assert get_resp.status_code == 404
    assert get_resp.json() == {"detail": "Review not found"}

