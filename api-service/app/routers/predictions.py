"""
Prediction router (View layer).
"""

from fastapi import APIRouter

from ..schemas import (
    PropertyInput,
    PredictionResponse,
    ModelInfoResponse,
    ErrorResponse
)
from ..controllers import PredictionController


router = APIRouter()


@router.get(
    "/model/info",
    response_model=ModelInfoResponse,
    summary="Model Information",
    description="Get detailed information about the loaded model"
)
async def model_info() -> ModelInfoResponse:
    """
    Model information endpoint.

    Returns metadata about the trained model.
    """
    from ..core import forecaster
    info = PredictionController.get_model_info(forecaster)
    return ModelInfoResponse(**info)


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict Property Price",
    description="Predict UK property price using Random Forest model",
    responses={
        200: {"description": "Prediction successful"},
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def predict_price(property_data: PropertyInput) -> PredictionResponse:
    """
    Main prediction endpoint.

    Args:
        property_data: Property information (PropertyInput schema)

    Returns:
        PredictionResponse with predicted price and confidence interval

    Raises:
        HTTPException: If prediction fails (handled by controller)
    """
    from ..core import forecaster
    data = property_data.model_dump()
    result = PredictionController.predict_price(forecaster, data)
    return PredictionResponse(**result)
