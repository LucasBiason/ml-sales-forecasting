"""
Pytest configuration and shared fixtures.
"""

from unittest.mock import MagicMock, Mock

import numpy as np
import pytest

from app.models.sales_forecaster import SalesForecaster


@pytest.fixture
def mock_model():
    """Create a mock Random Forest model."""
    model = MagicMock()
    model.n_estimators = 100
    model.estimators_ = [MagicMock() for _ in range(5)]
    for tree in model.estimators_:
        tree.predict.return_value = np.array([12.5])
    model.predict.return_value = np.array([12.5])
    return model


@pytest.fixture
def mock_label_encoders():
    """Create mock label encoders."""
    encoders = {"property_type": Mock(), "old_new": Mock(), "duration": Mock()}
    encoders["property_type"].transform.return_value = np.array([0])
    encoders["old_new"].transform.return_value = np.array([1])
    encoders["duration"].transform.return_value = np.array([0])
    return encoders


@pytest.fixture
def mock_target_encodings():
    """Create mock target encodings."""
    return {
        "county_map": {
            "GREATER LONDON": 450000.0,
            "SURREY": 420000.0,
            "UNKNOWN": 300000.0,
        },
        "postcode_map": {"SW1A": 500000.0, "SW1": 480000.0, "UNKNOWN": 300000.0},
    }


@pytest.fixture
def mock_metadata():
    """Create mock model metadata."""
    return {
        "features": [
            "property_type_enc",
            "county_enc",
            "postcode_region_enc",
            "old_new_enc",
            "duration_enc",
            "year",
        ],
        "model_type": "RandomForest",
        "training_samples": 99831,
        "cv_r2_mean": 0.4390,
        "expected_r2": 0.11,
        "trained_date": "2024-01-15",
    }


@pytest.fixture
def sample_property_data():
    """Sample property data for testing."""
    return {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }


@pytest.fixture
def forecaster_mock(
    mock_model, mock_label_encoders, mock_target_encodings, mock_metadata
):
    """Create a SalesForecaster instance with mocked dependencies."""
    forecaster = SalesForecaster(models_dir="tests/fixtures/models")
    forecaster.model = mock_model
    forecaster.label_encoders = mock_label_encoders
    forecaster.target_encodings = mock_target_encodings
    forecaster.metadata = mock_metadata
    forecaster.is_loaded = True
    return forecaster


@pytest.fixture
def forecaster_unloaded():
    """Create an unloaded SalesForecaster instance."""
    forecaster = SalesForecaster(models_dir="tests/fixtures/models")
    forecaster.is_loaded = False
    return forecaster
