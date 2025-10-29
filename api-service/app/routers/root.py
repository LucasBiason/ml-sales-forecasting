"""
Root router.
"""

from fastapi import APIRouter


router = APIRouter()


@router.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": "ML Sales Forecasting API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

