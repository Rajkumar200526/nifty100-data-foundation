from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_companies():
    response = client.get("/companies")

    assert response.status_code == 200
    assert isinstance(response.json(), list)