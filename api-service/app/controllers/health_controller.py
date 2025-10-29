"""
Health controller - system health and status.
"""

from datetime import datetime
from typing import Dict, Any


class HealthController:
    """Controller for health and system status operations."""

    @staticmethod
    def get_health_status(forecaster) -> Dict[str, Any]:
        """
        Get service health status.

        Args:
            forecaster: SalesForecaster instance

        Returns:
            Dictionary with health information
        """
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "model_loaded": forecaster.is_loaded,
            "version": "1.0.0"
        }
