import pytest  # noqa: F401
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app

client = TestClient(app)


# -------------------------
# Health check
# -------------------------
def test_health_check():
    """Проверяем, что сервер отвечает на GET /"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


# -------------------------
# Predict with a valid token
# -------------------------
def test_prediction_with_token():
    token = create_access_token()
    headers = {"Authorization": f"Bearer {token}"}

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

    response = client.post("/predict", json=sample, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data


# -------------------------
# Predict without a token
# -------------------------
def test_prediction_without_token():
    sample = {"longitude": 0, "latitude": 0}
    response = client.post("/predict", json=sample)
    assert response.status_code == 401


# -------------------------
# Predict with incorrect fields
# -------------------------
def test_prediction_with_invalid_data():
    token = create_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    invalid_sample = {"foo": "bar"}
    response = client.post("/predict", json=invalid_sample, headers=headers)
    assert response.status_code == 422


# -------------------------
# Rate limiting
# -------------------------
def test_rate_limit():
    token = create_access_token()
    headers = {"Authorization": f"Bearer {token}"}

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

    for i in range(6):
        response = client.post("/predict", json=sample, headers=headers)

    assert response.status_code == 429  # Too Many Requests
