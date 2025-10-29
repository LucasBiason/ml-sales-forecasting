"""
Prediction controller - ML prediction operations.
"""

from typing import Dict, Any
from fastapi import HTTPException, status


class PredictionController:
    """Controller for property price prediction operations."""

    @staticmethod
    def get_model_info(forecaster) -> Dict[str, Any]:
        """
        Get detailed model information.

        Args:
            forecaster: SalesForecaster instance

        Returns:
            Dictionary with model metadata
        """
        return forecaster.get_model_info()

    @staticmethod
    def predict_price(forecaster, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict property price.

        Args:
            forecaster: SalesForecaster instance
            property_data: Dictionary with property information

        Returns:
            Dictionary with prediction and confidence interval

        Raises:
            HTTPException: If model not loaded or prediction fails
        """
        if not forecaster.is_loaded:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not loaded. Please try again in a few seconds."
            )

        try:
            result = forecaster.predict(property_data)
            return result

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid data: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Prediction error: {str(e)}"
            )
