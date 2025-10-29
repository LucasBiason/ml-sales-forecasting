"""
Unit tests for HealthResponse schema.
"""

from datetime import datetime

from app.schemas.health import HealthResponse


def test_health_response_valid():
    """Test valid health response."""
    data = {
        "status": "healthy",
        "timestamp": datetime.now(),
        "model_loaded": True,
        "version": "1.0.0",
    }

    response = HealthResponse(**data)

    assert response.status == "healthy"
    assert response.model_loaded is True
    assert response.version == "1.0.0"
    assert isinstance(response.timestamp, datetime)


def test_health_response_model_unloaded():
    """Test health response when model is not loaded."""
    data = {
        "status": "healthy",
        "timestamp": datetime.now(),
        "model_loaded": False,
        "version": "1.0.0",
    }

    response = HealthResponse(**data)

    assert response.model_loaded is False
