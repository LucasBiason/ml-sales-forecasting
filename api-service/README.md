# ML Sales Forecasting API

FastAPI backend for UK property price prediction using Random Forest.

## Architecture

### MVC Pattern

```
app/
├── main.py                 # FastAPI application
├── core/                   # Lifecycle and configuration
│   └── lifecycle.py        # Model loading, startup/shutdown
├── models/                 # ML Models
│   └── sales_forecaster.py # SalesForecaster class
├── controllers/            # Business Logic
│   ├── health_controller.py
│   └── prediction_controller.py
├── routers/                # View Layer (Routes)
│   ├── root.py
│   ├── health.py
│   └── predictions.py
└── schemas/                # Pydantic Validation
    ├── property_input.py
    ├── prediction_response.py
    ├── health.py
    ├── model_info.py
    └── error.py
```

## Endpoints

### Root
- `GET /` - API information

### Health
- `GET /api/v1/health` - Health check and model status

### Predictions
- `GET /api/v1/model/info` - Model metadata and performance metrics
- `POST /api/v1/predict` - Predict property price

## Running Locally

```bash
# From project root
make deploy-models  # Copy trained models
make run-api        # Start FastAPI server
```

Or manually:

```bash
cd api-service
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Access:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
# From project root
./scripts/test_api.sh
```

## Example Request

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "property_type": "T",
    "old_new": "N",
    "duration": "F",
    "county": "GREATER LONDON",
    "postcode": "SW1A 1AA",
    "year": 2024
  }'
```

## Example Response

```json
{
  "predicted_price": 350267.88,
  "confidence_interval": {
    "min": 316447.07,
    "max": 400000.0
  },
  "features_used": [
    "property_type_enc",
    "county_enc",
    "postcode_region_enc",
    "old_new_enc",
    "duration_enc",
    "year"
  ],
  "model_info": {
    "type": "RandomForest",
    "n_estimators": 100,
    "expected_r2": 0.1116
  }
}
```

## Model Information

- **Type**: Random Forest Regressor
- **Estimators**: 100 trees
- **Training Samples**: 99,831
- **R² (general)**: 11.16%
- **R² (properties <£1M)**: 27%
- **MAE**: £86,796

## Requirements

See `requirements.txt` for dependencies.

Main dependencies:
- FastAPI 0.104+
- scikit-learn 1.3+
- Pydantic 2.5+
- uvicorn 0.24+

