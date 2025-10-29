.PHONY: help install deploy-models run-api test clean

help:
	@echo "ML Sales Forecasting - Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make install        - Install dependencies for notebooks and API"
	@echo "  make deploy-models  - Copy trained models from notebooks to API"
	@echo "  make run-api        - Start FastAPI server"
	@echo "  make test          - Run API tests"
	@echo "  make clean         - Clean cache and temporary files"

install:
	@echo "Installing notebook dependencies..."
	cd notebooks && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo ""
	@echo "Installing API dependencies..."
	cd api-service && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo ""
	@echo "✓ Installation complete!"

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
	@echo "Running API tests..."
	cd api-service && . venv/bin/activate && pytest tests/ -v

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete!"

