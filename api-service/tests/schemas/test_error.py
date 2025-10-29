"""
Unit tests for ErrorResponse schema.
"""

from datetime import datetime

from app.schemas.error import ErrorResponse


def test_error_response_valid():
    """Test valid error response."""
    data = {"detail": "Invalid property type", "error_type": "ValidationError"}

    response = ErrorResponse(**data)

    assert response.detail == "Invalid property type"
    assert response.error_type == "ValidationError"
    assert isinstance(response.timestamp, datetime)


def test_error_response_with_timestamp():
    """Test error response with explicit timestamp."""
    now = datetime.now()
    data = {
        "detail": "Model not loaded",
        "error_type": "ServiceError",
        "timestamp": now,
    }

    response = ErrorResponse(**data)

    assert response.timestamp == now
