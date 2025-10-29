.PHONY: help install deploy-models dev test build up down logs clean

help:
	@echo "ML Sales Forecasting - Makefile"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install notebook dependencies (venv)"
	@echo "  make deploy-models  - Copy trained models from notebooks to API"
	@echo ""
	@echo "Development:"
	@echo "  make dev            - Start API in dev mode (hot reload)"
	@echo "  make test           - Run tests (multi-stage build)"
	@echo "  make logs           - Show API logs"
	@echo ""
	@echo "Production:"
	@echo "  make build          - Build production image"
	@echo "  make up             - Start production API"
	@echo "  make down           - Stop containers"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          - Clean cache and temporary files"

install:
	@echo "Installing notebook dependencies (venv only)..."
	cd notebooks && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo ""
	@echo "✓ Notebook environment ready!"
	@echo ""
	@echo "NOTE: API runs ONLY in Docker. Use 'make dev' to start."

deploy-models:
	@echo "Deploying ML models to API..."
	python scripts/deploy_models.py
	@echo "✓ Models deployed!"

dev:
	@echo "Starting API in DEVELOPMENT mode (hot reload)..."
	@echo ""
	@ENVIRONMENT=development DEV_VOLUME=rw docker-compose --profile api up --build
	@echo ""
	@echo "API stopped."

test:
	@echo "Running tests (multi-stage build)..."
	@echo ""
	docker-compose --profile test build test
	docker-compose --profile test up --abort-on-container-exit test
	@echo ""
	@echo "Cleaning up..."
	docker-compose --profile test down
	@echo ""
	@echo "✓ Tests complete! Coverage: api-service/htmlcov/index.html"

build:
	@echo "Building PRODUCTION image (after tests)..."
	docker-compose --profile api build --no-cache api
	@echo "✓ Production image built!"

up:
	@echo "Starting PRODUCTION API..."
	@ENVIRONMENT=production DEV_VOLUME=ro docker-compose --profile api up -d
	@echo ""
	@echo "✓ API running!"
	@echo "  URL: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/docs"
	@echo ""
	@echo "View logs: make logs"

down:
	@echo "Stopping containers..."
	docker-compose --profile api down
	docker-compose --profile test down
	@echo "✓ Stopped!"

logs:
	@echo "API logs (Ctrl+C to exit):"
	@echo ""
	docker-compose --profile api logs -f api

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete!"

