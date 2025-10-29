#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status, treat unset variables as errors, and fail on pipeline errors.
set -euo pipefail

# Function to display CLI help
cli_help() {
  local cli_name=${0##*/}
  echo "
$cli_name
ML Sales Forecasting API - Entrypoint CLI
Usage: $cli_name [command]

Commands:
  test          Run tests with coverage (90%+ required)
  dev           Start development server (hot reload)
  runserver     Start production server (multi-worker)
  health        Check API health and model status
  *             Display this help message

Environment Variables:
  PORT          Server port (default: 8000)
  WORKERS       Number of workers for production (default: 4)
  LOG_LEVEL     Logging level (default: info)
"
  exit 1
}

# Function to check model files
check_models() {
  if [ ! -f "./models/final_model.joblib" ]; then
    echo "⚠️  WARNING: Model files not found in ./models/"
    echo "   Please run 'make deploy-models' first"
    return 1
  fi
  echo "✓ Model files found"
  return 0
}

# Main command handler
case "${1:-runserver}" in
  test)
    echo "========================================="
    echo "Running tests with coverage..."
    echo "========================================="
    pytest tests/ \
      --cov=app \
      --cov-report=term-missing \
      --cov-report=html \
      --cov-config=.coveragerc \
      --cov-fail-under=90 \
      -v
    ;;

  dev)
    echo "========================================="
    echo "ML Sales Forecasting API - DEVELOPMENT"
    echo "========================================="
    check_models || true
    PORT=${PORT:-8000}
    LOG_LEVEL=${LOG_LEVEL:-debug}
    
    echo "Starting development server..."
    echo "  Port: $PORT"
    echo "  Hot reload: enabled"
    echo "  Log level: $LOG_LEVEL"
    echo "========================================="
    
    exec uvicorn app.main:app \
      --host 0.0.0.0 \
      --port "$PORT" \
      --reload \
      --log-level "$LOG_LEVEL"
    ;;

  runserver)
    echo "========================================="
    echo "ML Sales Forecasting API - PRODUCTION"
    echo "========================================="
    check_models || exit 1
    
    PORT=${PORT:-8000}
    WORKERS=${WORKERS:-4}
    LOG_LEVEL=${LOG_LEVEL:-info}
    
    echo "Starting production server..."
    echo "  Port: $PORT"
    echo "  Workers: $WORKERS"
    echo "  Log level: $LOG_LEVEL"
    echo "========================================="
    
    exec uvicorn app.main:app \
      --host 0.0.0.0 \
      --port "$PORT" \
      --workers "$WORKERS" \
      --log-level "$LOG_LEVEL"
    ;;

  health)
    echo "========================================="
    echo "Health Check"
    echo "========================================="
    check_models
    echo "✓ API is ready to start"
    ;;

  *)
    cli_help
    ;;
esac


