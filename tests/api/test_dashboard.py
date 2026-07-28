from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_dashboard():
    response = client.get("/dashboard")

    # If authentication is required, this may return 401.
    # Otherwise it should return 200.
    assert response.status_code in [200, 401]