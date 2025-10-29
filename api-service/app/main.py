"""
FastAPI Application - ML Sales Forecasting API

API para predicao de precos de imoveis usando Random Forest.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .models import SalesForecaster
from .routers import health_router, predictions_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="ML Sales Forecasting API",
    description="API para predicao de precos de imoveis no Reino Unido usando Random Forest",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em producao, especificar origins permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar forecaster global
forecaster = SalesForecaster(models_dir="models")


@app.on_event("startup")
async def startup_event():
    """Carregar modelo na inicializacao."""
    try:
        logger.info("Carregando modelo...")
        forecaster.load()
        logger.info("Modelo carregado com sucesso!")
        logger.info(f"Model info: {forecaster.get_model_info()}")
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Limpar recursos no shutdown."""
    logger.info("Encerrando API...")


# Incluir routers
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(predictions_router, prefix="/api/v1", tags=["predictions"])


@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": "ML Sales Forecasting API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
