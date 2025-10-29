"""
API Routers.
"""

from .root import router as root_router
from .health import router as health_router
from .predictions import router as predictions_router

__all__ = ["root_router", "health_router", "predictions_router"]
