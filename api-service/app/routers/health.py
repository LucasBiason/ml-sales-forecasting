"""
Health check router (View layer).
"""

from fastapi import APIRouter

from ..controllers import HealthController
from ..schemas import HealthResponse

router = APIRouter()


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check (Root)",
    description="Check if service is running and model is loaded",
)
@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if service is running and model is loaded",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns service status and model loading state.
    Available at both / and /health.
    """
    from ..core import forecaster

    health_data = HealthController.get_health_status(forecaster)
    return HealthResponse(**health_data)
