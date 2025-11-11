import pytest  # noqa: F401
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# -------------------------
# General integration test
# -------------------------
def test_full_prediction_flow_e2e():
    response_token = client.get("/get_token")
    assert response_token.status_code == 200, "Token request failed"
    data_token = response_token.json()
    assert "access_token" in data_token
    token = data_token["access_token"]

    sample = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN",
    }

    headers = {"Authorization": f"Bearer {token}"}

    response_pred = client.post("/predict", json=sample, headers=headers)
    assert response_pred.status_code == 200, "Prediction request failed"
    result = response_pred.json()
    assert "prediction" in result
    assert isinstance(result["prediction"], list)
