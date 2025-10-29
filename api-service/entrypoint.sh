#!/bin/bash
set -e

# Entrypoint for ML Sales Forecasting API

echo "========================================="
echo "ML Sales Forecasting API"
echo "Environment: ${ENVIRONMENT:-production}"
echo "========================================="

# Check if models are loaded
if [ ! -f "./models/final_model.joblib" ]; then
    echo "WARNING: Model files not found in ./models/"
    echo "Please run 'make deploy-models' first"
fi

# Start application based on environment
if [ "${ENVIRONMENT}" = "development" ]; then
    echo "Starting in DEVELOPMENT mode (hot reload)..."
    exec uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload \
        --log-level debug
else
    echo "Starting in PRODUCTION mode..."
    exec uvicorn app.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --workers 4 \
        --log-level info
fi

