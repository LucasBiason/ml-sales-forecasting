.PHONY: help install deploy-models dev build up down logs test test-docker clean

help:
	@echo "ML Sales Forecasting - Makefile"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install notebook dependencies (venv)"
	@echo "  make deploy-models  - Copy trained models from notebooks to API"
	@echo ""
	@echo "Development (Docker):"
	@echo "  make dev            - Start API in development mode (hot reload)"
	@echo "  make logs           - Show API logs (Ctrl+C to exit)"
	@echo "  make test           - Run tests in Docker container"
	@echo ""
	@echo "Production (Docker):"
	@echo "  make build          - Build production Docker image"
	@echo "  make up             - Start production containers"
	@echo "  make down           - Stop and remove containers"
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
	@echo "Starting API in development mode (Docker with hot reload)..."
	@echo ""
	docker-compose up --build
	@echo ""
	@echo "API stopped. Use 'make down' to cleanup containers."

build:
	@echo "Building production Docker image..."
	docker-compose build --no-cache
	@echo "✓ Production image built!"

up:
	@echo "Starting production containers..."
	docker-compose up -d
	@echo ""
	@echo "✓ API running in production mode!"
	@echo "  URL: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/docs"
	@echo ""
	@echo "View logs: make logs"

down:
	@echo "Stopping all containers..."
	docker-compose down
	@echo "✓ Containers stopped and removed!"

logs:
	@echo "API logs (Ctrl+C to exit):"
	@echo ""
	docker-compose logs -f api

test:
	@echo "Running tests in Docker container..."
	@echo ""
	docker-compose -f docker-compose.test.yml build
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit
	@echo ""
	@echo "Cleaning up..."
	docker-compose -f docker-compose.test.yml down
	@echo ""
	@echo "✓ Tests complete! Coverage: api-service/htmlcov/index.html"

test-docker: test

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete!"

