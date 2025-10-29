.PHONY: help install install-dev deploy-models run-api test test-docker clean docker-build docker-up docker-down docker-logs docker-test

help:
	@echo "ML Sales Forecasting - Makefile"
	@echo ""
	@echo "Local Development:"
	@echo "  make install        - Install production dependencies"
	@echo "  make install-dev    - Install dev dependencies (includes tests)"
	@echo "  make deploy-models  - Copy trained models from notebooks to API"
	@echo "  make run-api        - Start FastAPI server (local)"
	@echo "  make test           - Run API tests locally"
	@echo "  make test-docker    - Run tests in Docker container (CI/CD)"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-build   - Build production Docker image"
	@echo "  make docker-up      - Start production containers"
	@echo "  make docker-down    - Stop and remove containers"
	@echo "  make docker-logs    - Show container logs"
	@echo "  make docker-test    - Test production API in Docker"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          - Clean cache and temporary files"

install:
	@echo "Installing production dependencies..."
	cd api-service && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Production dependencies installed!"

install-dev:
	@echo "Installing notebook dependencies..."
	cd notebooks && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo ""
	@echo "Installing API dev dependencies..."
	cd api-service && python -m venv venv && . venv/bin/activate && pip install -r requirements-dev.txt
	@echo ""
	@echo "✓ Dev installation complete!"

deploy-models:
	@echo "Deploying ML models to API..."
	python scripts/deploy_models.py
	@echo "✓ Models deployed!"

run-api:
	@echo "Starting FastAPI server..."
	@echo "API will be available at: http://localhost:8000"
	@echo "Docs at: http://localhost:8000/docs"
	cd api-service && . venv/bin/activate && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

test:
	@echo "Running API tests with coverage..."
	cd api-service && python -m pytest tests/ -v --tb=short
	@echo ""
	@echo "Coverage report generated in api-service/htmlcov/index.html"

test-docker:
	@echo "Building test Docker image..."
	docker-compose -f docker-compose.test.yml build
	@echo ""
	@echo "Running tests in Docker container..."
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit
	@echo ""
	@echo "Cleaning up test containers..."
	docker-compose -f docker-compose.test.yml down
	@echo "✓ Docker tests complete! Coverage report in api-service/htmlcov/"

docker-build:
	@echo "Building Docker images..."
	docker-compose build
	@echo "✓ Images built!"

docker-up:
	@echo "Starting containers with docker-compose..."
	docker-compose up -d
	@echo ""
	@echo "✓ Containers started!"
	@echo "API available at: http://localhost:8000"
	@echo "Docs at: http://localhost:8000/docs"
	@echo ""
	@echo "Check status with: make docker-logs"

docker-down:
	@echo "Stopping containers..."
	docker-compose down
	@echo "✓ Containers stopped!"

docker-logs:
	@echo "Container logs (Ctrl+C to exit):"
	docker-compose logs -f api

docker-test:
	@echo "Testing API in Docker..."
	@sleep 3
	@curl -s http://localhost:8000/health | python -m json.tool || echo "API not responding"

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete!"

