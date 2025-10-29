"""
Core module - lifecycle and configuration.
"""

from .lifecycle import startup_event, shutdown_event, forecaster

__all__ = ["startup_event", "shutdown_event", "forecaster"]

