from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_stock_trends():
    response = client.get("/stock-trends/1")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        assert "trade_date" in data[0]
        assert "close_price" in data[0]