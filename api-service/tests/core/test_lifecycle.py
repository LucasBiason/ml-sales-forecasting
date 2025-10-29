"""
Unit tests for lifecycle events.
"""

from unittest.mock import patch

import pytest

from app.core.lifecycle import forecaster, shutdown_event, startup_event


@pytest.mark.asyncio
async def test_startup_event_success():
    """Test successful startup event."""
    with patch.object(forecaster, "load") as mock_load:
        with patch.object(
            forecaster,
            "get_model_info",
            return_value={"loaded": True, "model_type": "RandomForest"},
        ):
            await startup_event()
            mock_load.assert_called_once()


@pytest.mark.asyncio
async def test_startup_event_failure():
    """Test startup event when model loading fails."""
    with patch.object(forecaster, "load", side_effect=Exception("Model not found")):
        with pytest.raises(Exception, match="Model not found"):
            await startup_event()


@pytest.mark.asyncio
async def test_shutdown_event():
    """Test shutdown event."""
    with patch("app.core.lifecycle.logger") as mock_logger:
        await shutdown_event()
        mock_logger.info.assert_called_once_with("Shutting down API...")


def test_forecaster_initialization():
    """Test forecaster is initialized with correct models directory."""
    assert forecaster is not None
    assert str(forecaster.models_dir) == "models"
