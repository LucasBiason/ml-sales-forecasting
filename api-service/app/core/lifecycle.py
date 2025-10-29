"""
Application lifecycle events.

Handles model loading on startup and cleanup on shutdown.
"""

import logging

from ..models import SalesForecaster

logger = logging.getLogger(__name__)

# Initialize forecaster global
forecaster = SalesForecaster(models_dir="models")


async def startup_event():
    """Load ML model on application startup."""
    try:
        logger.info("Loading model...")
        forecaster.load()
        logger.info("Model loaded successfully!")
        logger.info(f"Model info: {forecaster.get_model_info()}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise


async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down API...")
