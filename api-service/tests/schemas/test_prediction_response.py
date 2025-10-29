"""
Unit tests for PredictionResponse schema.
"""

import pytest
from pydantic import ValidationError

from app.schemas.prediction_response import (
    ConfidenceInterval,
    ModelInfo,
    PredictionResponse
)


def test_confidence_interval_valid():
    """Test valid confidence interval."""
    data = {"min": 350000.0, "max": 450000.0}
    interval = ConfidenceInterval(**data)

    assert interval.min == 350000.0
    assert interval.max == 450000.0


def test_model_info_valid():
    """Test valid model info."""
    data = {
        "type": "RandomForest",
        "n_estimators": 100,
        "expected_r2": 0.11
    }
    info = ModelInfo(**data)

    assert info.type == "RandomForest"
    assert info.n_estimators == 100
    assert info.expected_r2 == 0.11


def test_prediction_response_valid():
    """Test valid prediction response."""
    data = {
        "predicted_price": 425000.50,
        "confidence_interval": {"min": 380000.00, "max": 470000.00},
        "features_used": ["property_type_enc", "county_enc"],
        "model_info": {
            "type": "RandomForest",
            "n_estimators": 100,
            "expected_r2": 0.11
        }
    }

    response = PredictionResponse(**data)

    assert response.predicted_price == 425000.50
    assert response.confidence_interval.min == 380000.00
    assert response.confidence_interval.max == 470000.00
    assert len(response.features_used) == 2
    assert response.model_info.type == "RandomForest"


def test_prediction_response_missing_field():
    """Test prediction response with missing field."""
    data = {
        "predicted_price": 425000.50,
        # Missing confidence_interval
        "features_used": ["property_type_enc"],
        "model_info": {
            "type": "RandomForest",
            "n_estimators": 100,
            "expected_r2": 0.11
        }
    }

    with pytest.raises(ValidationError):
        PredictionResponse(**data)

