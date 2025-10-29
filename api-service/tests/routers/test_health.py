"""
Unit tests for health router.
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
def test_health_check_root(mock_forecaster, client):
    """Test health check endpoint at root."""
    mock_forecaster.is_loaded = True

    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


@patch("app.core.forecaster")
def test_health_check_endpoint(mock_forecaster, client):
    """Test health check endpoint at /health."""
    mock_forecaster.is_loaded = True

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


@patch("app.core.forecaster")
def test_health_check_unloaded(mock_forecaster, client):
    """Test health check when model is not loaded."""
    mock_forecaster.is_loaded = False

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["model_loaded"] is False
