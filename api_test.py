from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello API!"}

def test_login():
    response = client.post("/api/login", params={
        "username": "admin",
        "password": "1234"
    })
    assert response.status_code == 200
