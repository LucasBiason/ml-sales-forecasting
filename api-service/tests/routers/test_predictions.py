"""
Unit tests for predictions router.
"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@patch("app.core.forecaster")
def test_model_info_loaded(mock_forecaster, client):
    """Test model info endpoint when loaded."""
    mock_forecaster.is_loaded = True
    mock_forecaster.get_model_info.return_value = {
        "loaded": True,
        "model_type": "RandomForest",
        "n_estimators": 100,
        "features": ["property_type_enc", "county_enc"],
        "expected_r2": 0.11,
    }

    response = client.get("/api/v1/model/info")

    assert response.status_code == 200
    data = response.json()
    assert data["loaded"] is True
    assert data["model_type"] == "RandomForest"
    assert data["n_estimators"] == 100


@patch("app.core.forecaster")
def test_model_info_unloaded(mock_forecaster, client):
    """Test model info endpoint when not loaded."""
    mock_forecaster.is_loaded = False
    mock_forecaster.get_model_info.return_value = {"loaded": False}

    response = client.get("/api/v1/model/info")

    assert response.status_code == 200
    data = response.json()
    assert data["loaded"] is False


@patch("app.core.forecaster")
def test_predict_success(mock_forecaster, client):
    """Test successful prediction."""
    mock_forecaster.is_loaded = True
    mock_forecaster.predict.return_value = {
        "predicted_price": 425000.50,
        "confidence_interval": {"min": 380000.00, "max": 470000.00},
        "features_used": ["property_type_enc", "county_enc"],
        "model_info": {
            "type": "RandomForest",
            "n_estimators": 100,
            "expected_r2": 0.11,
        },
    }

    payload = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] == 425000.50
    assert "confidence_interval" in data
    assert "min" in data["confidence_interval"]
    assert "max" in data["confidence_interval"]


@patch("app.core.forecaster")
def test_predict_invalid_property_type(mock_forecaster, client):
    """Test prediction with invalid property type."""
    mock_forecaster.is_loaded = True

    payload = {
        "property_type": "X",  # Invalid: must be D/S/T/F/O
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422
    assert "property_type" in str(response.json())


@patch("app.core.forecaster")
def test_predict_invalid_year(mock_forecaster, client):
    """Test prediction with invalid year (out of range)."""
    mock_forecaster.is_loaded = True

    payload = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 1990,  # Invalid: must be >= 1995
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422


@patch("app.core.forecaster")
def test_predict_missing_fields(mock_forecaster, client):
    """Test prediction with missing required fields."""
    mock_forecaster.is_loaded = True

    payload = {
        "property_type": "T"
        # Missing other required fields
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422


@patch("app.core.forecaster")
def test_predict_model_not_loaded(mock_forecaster, client):
    """Test prediction when model is not loaded."""
    mock_forecaster.is_loaded = False

    payload = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 503
    assert "Model not loaded" in response.json()["detail"]


@patch("app.core.forecaster")
def test_predict_postcode_normalization(mock_forecaster, client):
    """Test postcode normalization (uppercase and trim)."""
    mock_forecaster.is_loaded = True
    mock_forecaster.predict.return_value = {
        "predicted_price": 400000.0,
        "confidence_interval": {"min": 350000.0, "max": 450000.0},
        "features_used": [],
        "model_info": {
            "type": "RandomForest",
            "n_estimators": 100,
            "expected_r2": 0.11,
        },
    }

    payload = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "greater london",  # Should be normalized to uppercase
        "postcode": "sw1a 1aa",  # Should be normalized (without extra spaces)
        "year": 2024,
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 200
