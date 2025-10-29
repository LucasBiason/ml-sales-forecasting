"""
Unit tests for ModelInfoResponse schema.
"""

from app.schemas.model_info import ModelInfoResponse


def test_model_info_response_loaded():
    """Test model info response when loaded."""
    data = {
        "loaded": True,
        "model_type": "RandomForest",
        "n_estimators": 100,
        "features": ["property_type_enc", "county_enc"],
        "training_samples": 99831,
        "cv_r2_mean": 0.4390,
        "expected_r2": 0.11,
        "trained_date": "2024-01-15",
    }

    response = ModelInfoResponse(**data)

    assert response.loaded is True
    assert response.model_type == "RandomForest"
    assert response.n_estimators == 100
    assert len(response.features) == 2
    assert response.training_samples == 99831


def test_model_info_response_unloaded():
    """Test model info response when not loaded."""
    data = {"loaded": False}

    response = ModelInfoResponse(**data)

    assert response.loaded is False
    assert response.model_type is None
    assert response.n_estimators is None


def test_model_info_response_optional_fields():
    """Test model info response with some optional fields."""
    data = {"loaded": True, "model_type": "RandomForest", "n_estimators": 100}

    response = ModelInfoResponse(**data)

    assert response.loaded is True
    assert response.features is None
    assert response.cv_r2_mean is None
