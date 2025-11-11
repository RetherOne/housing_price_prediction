from time import sleep

import pytest  # noqa: F401
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app

client = TestClient(app)


# -------------------------
# Health check
# -------------------------
def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


# -------------------------
# Get tocken check
# -------------------------
def test_get_tocken_check():
    response = client.get("/get_token")
    assert response.status_code == 200
    assert "access_token" in response.json()


# -------------------------
# Predicts with a valid token
# -------------------------
def test_prediction_with_input1():
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
    assert isinstance(data["prediction"], list)


def test_prediction_with_input2():
    token = create_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    sample = {
        "longitude": -115.73,
        "latitude": 33.35,
        "housing_median_age": 23.0,
        "total_rooms": 1586.0,
        "total_bedrooms": 448.0,
        "population": 338.0,
        "households": 182.0,
        "median_income": 1.2132,
        "ocean_proximity": "INLAND",
    }

    response = client.post("/predict", json=sample, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert isinstance(data["prediction"], list)


def test_prediction_with_input3():
    token = create_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    sample = {
        "longitude": -117.96,
        "latitude": 33.89,
        "housing_median_age": 24.0,
        "total_rooms": 1332.0,
        "total_bedrooms": 252.0,
        "population": 625.0,
        "households": 230.0,
        "median_income": 4.4375,
        "ocean_proximity": "<1H OCEAN",
    }

    response = client.post("/predict", json=sample, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert isinstance(data["prediction"], list)


def test_prediction_with_input4():
    token = create_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    sample = [
        {
            "longitude": -122.64,
            "latitude": 38.01,
            "housing_median_age": 36.0,
            "total_rooms": 1336.0,
            "total_bedrooms": 258.0,
            "population": 678.0,
            "households": 249.0,
            "median_income": 5.5789,
            "ocean_proximity": "NEAR OCEAN",
        },
        {
            "longitude": -115.73,
            "latitude": 33.35,
            "housing_median_age": 23.0,
            "total_rooms": 1586.0,
            "total_bedrooms": 448.0,
            "population": 338.0,
            "households": 182.0,
            "median_income": 1.2132,
            "ocean_proximity": "INLAND",
        },
        {
            "longitude": -117.96,
            "latitude": 33.89,
            "housing_median_age": 24.0,
            "total_rooms": 1332.0,
            "total_bedrooms": 252.0,
            "population": 625.0,
            "households": 230.0,
            "median_income": 4.4375,
            "ocean_proximity": "<1H OCEAN",
        },
    ]

    response = client.post("/predict", json=sample, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert isinstance(data["prediction"], list)


# -------------------------
# Predict without a token
# -------------------------
def test_prediction_without_token():
    sample = {"foo": 0}
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
        sleep(0.1)

    assert response.status_code == 429  # Too Many Requests
