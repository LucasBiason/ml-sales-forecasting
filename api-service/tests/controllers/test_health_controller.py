"""
Unit tests for HealthController.
"""

from datetime import datetime
from unittest.mock import MagicMock

from app.controllers.health_controller import HealthController
from app.models.sales_forecaster import SalesForecaster


def test_get_health_status_loaded():
    """Test health status when model is loaded."""
    forecaster = MagicMock(spec=SalesForecaster)
    forecaster.is_loaded = True

    result = HealthController.get_health_status(forecaster)

    assert result["status"] == "healthy"
    assert result["model_loaded"] is True
    assert result["version"] == "1.0.0"
    assert isinstance(result["timestamp"], datetime)


def test_get_health_status_unloaded():
    """Test health status when model is not loaded."""
    forecaster = MagicMock(spec=SalesForecaster)
    forecaster.is_loaded = False

    result = HealthController.get_health_status(forecaster)

    assert result["status"] == "healthy"
    assert result["model_loaded"] is False
    assert result["version"] == "1.0.0"
