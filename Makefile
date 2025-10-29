.PHONY: help install deploy-models dev dev-full test build up up-full down logs clean

help:
	@echo "ML Sales Forecasting - Makefile"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install notebook dependencies (venv)"
	@echo "  make deploy-models  - Copy trained models from notebooks to API"
	@echo ""
	@echo "Development:"
	@echo "  make dev            - Start API only (hot reload)"
	@echo "  make dev-full       - Start API + Frontend (full stack)"
	@echo "  make test           - Run tests (multi-stage build)"
	@echo "  make logs           - Show API logs"
	@echo ""
	@echo "Production:"
	@echo "  make build          - Build all images (API + Frontend)"
	@echo "  make up             - Start API only"
	@echo "  make up-full        - Start API + Frontend"
	@echo "  make down           - Stop all containers"
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
	@API_COMMAND=dev DEV_VOLUME=rw LOG_LEVEL=debug docker-compose --profile api up --build
	@echo ""
	@echo "API stopped."

dev-full:
	@echo "Starting FULL STACK in DEVELOPMENT mode..."
	@echo ""
	@API_COMMAND=dev DEV_VOLUME=rw LOG_LEVEL=debug docker-compose --profile full up --build
	@echo ""
	@echo "Services stopped."

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
	@echo "Building PRODUCTION images..."
	docker-compose build --no-cache api frontend
	@echo "✓ Production images built!"

up:
	@echo "Starting PRODUCTION API..."
	@API_COMMAND=runserver DEV_VOLUME=ro WORKERS=4 LOG_LEVEL=info docker-compose --profile api up -d
	@echo ""
	@echo "✓ API running!"
	@echo "  URL: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/docs"
	@echo ""
	@echo "View logs: make logs"

up-full:
	@echo "Starting FULL STACK in PRODUCTION..."
	@API_COMMAND=runserver DEV_VOLUME=ro WORKERS=4 LOG_LEVEL=info docker-compose --profile full up -d
	@echo ""
	@echo "✓ Full stack running!"
	@echo "  Frontend: http://localhost:3000"
	@echo "  API: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/docs"
	@echo ""
	@echo "View logs: make logs"

down:
	@echo "Stopping all containers..."
	docker-compose --profile api down
	docker-compose --profile frontend down
	docker-compose --profile full down
	docker-compose --profile test down
	@echo "✓ Stopped!"

logs:
	@echo "Logs (Ctrl+C to exit):"
	@echo ""
	docker-compose logs -f api frontend 2>/dev/null || docker-compose --profile api logs -f api

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete!"

