# Multi-stage Dockerfile for ML Sales Forecasting API

# ============================================
# Stage 1: Base - Dependencies
# ============================================
FROM python:3.13-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ============================================
# Stage 2: Test - Run tests with coverage
# ============================================
FROM base AS test

# Install dev dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy application code
COPY app/ ./app/

# Copy tests
COPY tests/ ./tests/
COPY pytest.ini .coveragerc ./

# Copy models for testing
COPY models/ ./models/

# Run tests
RUN pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=90


# ============================================
# Stage 3: Production - Clean and minimal
# ============================================
FROM base AS production

# Copy only production code (no tests)
COPY app/ ./app/
COPY models/ ./models/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
