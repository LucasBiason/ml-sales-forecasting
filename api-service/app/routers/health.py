"""
Health check router (View layer).
"""

from fastapi import APIRouter

from ..schemas import HealthResponse
from ..controllers import HealthController


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if service is running and model is loaded"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns service status and model loading state.
    """
    from ..core import forecaster
    health_data = HealthController.get_health_status(forecaster)
    return HealthResponse(**health_data)
