"""
Core module - lifecycle and configuration.
"""

from .lifecycle import forecaster, shutdown_event, startup_event

__all__ = ["startup_event", "shutdown_event", "forecaster"]
