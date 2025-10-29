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
# Stage 2: Test - Prepare test environment
# ============================================
FROM base AS test

# Install dev dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy application code (including all __init__.py)
COPY app/ ./app/

# Copy tests
COPY tests/ ./tests/
COPY pytest.ini .coveragerc ./

# Copy models directory (may be empty in CI)
COPY models ./models

# Copy entrypoint
COPY --chmod=755 entrypoint.sh /entrypoint.sh

# Set PYTHONPATH for imports
ENV PYTHONPATH=/app

# Tests run via entrypoint (not during build)
ENTRYPOINT ["/entrypoint.sh"]
CMD ["test"]


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

# Copy and set entrypoint
COPY --chmod=755 entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["runserver"]
