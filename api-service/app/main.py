"""
FastAPI Application - ML Sales Forecasting API.

API for UK property price prediction using Random Forest.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .core import startup_event, shutdown_event
from .routers import root_router, health_router, predictions_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Initialize FastAPI
app = FastAPI(
    title="ML Sales Forecasting API",
    description="API for UK property price prediction using Random Forest",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifecycle events
app.on_event("startup")(startup_event)
app.on_event("shutdown")(shutdown_event)

# Include routers
app.include_router(root_router)
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(predictions_router, prefix="/api/v1", tags=["predictions"])
