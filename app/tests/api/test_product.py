from app.main import  app
from fastapi.testclient import TestClient

# test data
start_date_str = "2023-11-14"
end_date_str = "2023-11-15"
key_product = "1|60925"

client = TestClient(app,  headers={"Authorization": "Bearer token"})
response = client.get(f"/sales-by-product?key_product={key_product}&start_date_str={start_date_str}&end_date_str={end_date_str}",)

def test_response_status_code():
    assert response.status_code == 200


def test_data_structure():
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_keys_in_data():
    data = response.json()
    for sale_data in data:
        assert "KeySale" in sale_data
        assert "KeyDate" in sale_data
        assert "KeyStore" in sale_data