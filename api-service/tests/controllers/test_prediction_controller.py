"""
Unit tests for PredictionController.
"""

import pytest
from fastapi import HTTPException, status

from app.controllers.prediction_controller import PredictionController


def test_get_model_info_success(forecaster_mock):
    """Test getting model info successfully."""
    result = PredictionController.get_model_info(forecaster_mock)

    assert result["loaded"] is True
    assert "model_type" in result
    assert "n_estimators" in result


def test_predict_price_success(forecaster_mock, sample_property_data):
    """Test successful price prediction."""
    result = PredictionController.predict_price(forecaster_mock, sample_property_data)

    assert "predicted_price" in result
    assert "confidence_interval" in result
    assert "features_used" in result
    assert "model_info" in result


def test_predict_price_model_not_loaded(forecaster_unloaded, sample_property_data):
    """Test prediction when model is not loaded."""
    with pytest.raises(HTTPException) as exc_info:
        PredictionController.predict_price(forecaster_unloaded, sample_property_data)

    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "Model not loaded" in exc_info.value.detail


def test_predict_price_value_error(sample_property_data):
    """Test prediction with ValueError (invalid data)."""
    from unittest.mock import MagicMock
    
    forecaster_mock = MagicMock()
    forecaster_mock.is_loaded = True
    forecaster_mock.predict = MagicMock(side_effect=ValueError("Invalid county"))

    with pytest.raises(HTTPException) as exc_info:
        PredictionController.predict_price(forecaster_mock, sample_property_data)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid data" in exc_info.value.detail


def test_predict_price_generic_error(sample_property_data):
    """Test prediction with generic error."""
    from unittest.mock import MagicMock
    
    forecaster_mock = MagicMock()
    forecaster_mock.is_loaded = True
    forecaster_mock.predict = MagicMock(side_effect=Exception("Unexpected error"))

    with pytest.raises(HTTPException) as exc_info:
        PredictionController.predict_price(forecaster_mock, sample_property_data)

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Prediction error" in exc_info.value.detail
