# ML Sales Forecasting API - Postman Documentation

Complete API documentation with real request/response examples.

---

## Base URL

```
http://localhost:8000
```

In production, replace with your deployed URL.

---

## Table of Contents

1. [Root Endpoints](#root-endpoints)
2. [Health Endpoints](#health-endpoints)
3. [Prediction Endpoints](#prediction-endpoints)
4. [Error Responses](#error-responses)

---

## Root Endpoints

### GET / - API Information

Get basic API information and available endpoints.

**Request:**
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
    "message": "ML Sales Forecasting API",
    "version": "1.0.0",
    "docs": "/docs",
    "health": "/api/v1/health"
}
```

---

## Health Endpoints

### GET /api/v1/health - Health Check

Check if service is running and model is loaded.

**Request:**
```http
GET /api/v1/health HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
    "status": "healthy",
    "timestamp": "2025-10-29T10:23:34.730372",
    "model_loaded": true,
    "version": "1.0.0"
}
```

**Fields:**
- `status` (string): Service status ("healthy" or "unhealthy")
- `timestamp` (datetime): Response timestamp in ISO 8601 format
- `model_loaded` (boolean): Whether ML model is loaded in memory
- `version` (string): API version

---

### GET /api/v1/model/info - Model Information

Get detailed metadata about the loaded ML model.

**Request:**
```http
GET /api/v1/model/info HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**
```json
{
    "loaded": true,
    "model_type": "RandomForestRegressor",
    "n_estimators": 100,
    "features": [
        "property_type_enc",
        "county_enc",
        "postcode_region_enc",
        "old_new_enc",
        "duration_enc",
        "year"
    ],
    "training_samples": 99831,
    "cv_r2_mean": 0.43903378976114366,
    "expected_r2": 0.1116,
    "trained_date": "2025-10-28T20:09:54.055543"
}
```

**Fields:**
- `loaded` (boolean): Whether model is loaded
- `model_type` (string): Type of ML model (RandomForestRegressor)
- `n_estimators` (integer): Number of trees in the forest
- `features` (array): List of features used by the model
- `training_samples` (integer): Number of samples used for training
- `cv_r2_mean` (float): Mean R² score from cross-validation (log scale)
- `expected_r2` (float): Expected R² score on original price scale
- `trained_date` (string): Date when model was trained (ISO 8601)

---

## Prediction Endpoints

### POST /api/v1/predict - Predict Property Price

Predict UK property price using Random Forest model.

**Request:**
```http
POST /api/v1/predict HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "property_type": "T",
    "old_new": "N",
    "duration": "F",
    "county": "GREATER LONDON",
    "postcode": "SW1A 1AA",
    "year": 2024
}
```

**Request Fields:**

| Field | Type | Required | Description | Valid Values |
|-------|------|----------|-------------|--------------|
| `property_type` | string | Yes | Property type | D=Detached, S=Semi-detached, T=Terraced, F=Flat, O=Other |
| `old_new` | string | Yes | New or existing | Y=New construction, N=Existing property |
| `duration` | string | Yes | Tenure type | F=Freehold, L=Leasehold, U=Unknown |
| `county` | string | Yes | Property county | Any UK county (e.g. "GREATER LONDON", "SURREY") |
| `postcode` | string | Yes | Full UK postcode | Format: "SW1A 1AA" (will be normalized to uppercase) |
| `year` | integer | Yes | Sale year | Between 1995 and 2030 |

**Response (200 OK):**
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

**Response Fields:**
- `predicted_price` (float): Predicted price in GBP (£)
- `confidence_interval` (object): Prediction confidence bounds
  - `min` (float): Lower bound (10th percentile across trees)
  - `max` (float): Upper bound (90th percentile across trees)
- `features_used` (array): List of features used for this prediction
- `model_info` (object): Information about the model
  - `type` (string): Model type
  - `n_estimators` (integer): Number of trees
  - `expected_r2` (float): Expected R² score

---

## Example Scenarios

### Scenario 1: Terraced House in Greater London

**Request:**
```json
{
    "property_type": "T",
    "old_new": "N",
    "duration": "F",
    "county": "GREATER LONDON",
    "postcode": "SW1A 1AA",
    "year": 2024
}
```

**Response:**
```json
{
    "predicted_price": 350267.88,
    "confidence_interval": {
        "min": 316447.07,
        "max": 400000.0
    }
}
```

**Interpretation:** Terraced house in central London, predicted at £350k with range £316k-£400k.

---

### Scenario 2: Detached House in Surrey (Expensive Area)

**Request:**
```json
{
    "property_type": "D",
    "old_new": "Y",
    "duration": "F",
    "county": "SURREY",
    "postcode": "GU1 1AA",
    "year": 2024
}
```

**Response:**
```json
{
    "predicted_price": 1061889.77,
    "confidence_interval": {
        "min": 479999.5,
        "max": 2322500.0
    }
}
```

**Interpretation:** New detached house in Surrey, predicted at £1.06M with wide range £480k-£2.3M (reflects market variability).

---

### Scenario 3: Flat in Greater Manchester (Cheaper Area)

**Request:**
```json
{
    "property_type": "F",
    "old_new": "N",
    "duration": "L",
    "county": "GREATER MANCHESTER",
    "postcode": "M1 1AA",
    "year": 2024
}
```

**Response:**
```json
{
    "predicted_price": 236572.01,
    "confidence_interval": {
        "min": 230000.0,
        "max": 245000.0
    }
}
```

**Interpretation:** Leasehold flat in Manchester, predicted at £236k with narrow range (more confident prediction).

---

## Error Responses

### 422 Validation Error - Invalid Property Type

**Request:**
```json
{
    "property_type": "X",
    "old_new": "N",
    "duration": "F",
    "county": "GREATER LONDON",
    "postcode": "SW1A 1AA",
    "year": 2024
}
```

**Response (422 Unprocessable Entity):**
```json
{
    "detail": [
        {
            "type": "string_pattern_mismatch",
            "loc": ["body", "property_type"],
            "msg": "String should match pattern '^[DSTFO]$'",
            "input": "X",
            "ctx": {
                "pattern": "^[DSTFO]$"
            }
        }
    ]
}
```

**Explanation:** Property type must be one of: D, S, T, F, or O.

---

### 422 Validation Error - Missing Required Fields

**Request:**
```json
{
    "property_type": "T",
    "old_new": "N",
    "duration": "F",
    "year": 2024
}
```

**Response (422 Unprocessable Entity):**
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "county"],
            "msg": "Field required",
            "input": {
                "property_type": "T",
                "old_new": "N",
                "duration": "F",
                "year": 2024
            }
        },
        {
            "type": "missing",
            "loc": ["body", "postcode"],
            "msg": "Field required",
            "input": {
                "property_type": "T",
                "old_new": "N",
                "duration": "F",
                "year": 2024
            }
        }
    ]
}
```

**Explanation:** Both `county` and `postcode` are required fields.

---

### 422 Validation Error - Invalid Year Range

**Request:**
```json
{
    "property_type": "T",
    "old_new": "N",
    "duration": "F",
    "county": "GREATER LONDON",
    "postcode": "SW1A 1AA",
    "year": 1990
}
```

**Response (422 Unprocessable Entity):**
```json
{
    "detail": [
        {
            "type": "greater_than_equal",
            "loc": ["body", "year"],
            "msg": "Input should be greater than or equal to 1995",
            "input": 1990,
            "ctx": {
                "ge": 1995
            }
        }
    ]
}
```

**Explanation:** Year must be between 1995 and 2030 (model training range).

---

## Field Validation Rules

### property_type
- **Type:** String (1 character)
- **Pattern:** `^[DSTFO]$`
- **Valid values:**
  - `D` - Detached
  - `S` - Semi-detached
  - `T` - Terraced
  - `F` - Flat/Apartment
  - `O` - Other
- **Case sensitive:** Yes (must be uppercase)

### old_new
- **Type:** String (1 character)
- **Pattern:** `^[YN]$`
- **Valid values:**
  - `Y` - New construction
  - `N` - Existing property
- **Case sensitive:** Yes (must be uppercase)

### duration
- **Type:** String (1 character)
- **Pattern:** `^[FLU]$`
- **Valid values:**
  - `F` - Freehold
  - `L` - Leasehold
  - `U` - Unknown
- **Case sensitive:** Yes (must be uppercase)

### county
- **Type:** String
- **Min length:** 2 characters
- **Max length:** 50 characters
- **Normalization:** Automatically converted to uppercase
- **Examples:** "GREATER LONDON", "SURREY", "GREATER MANCHESTER"

### postcode
- **Type:** String
- **Min length:** 5 characters
- **Max length:** 10 characters
- **Format:** UK postcode format (e.g. "SW1A 1AA", "M1 1AA", "GU1 1AA")
- **Normalization:** Automatically converted to uppercase and trimmed

### year
- **Type:** Integer
- **Min value:** 1995
- **Max value:** 2030
- **Description:** Year of property sale

---

## Postman Collection Import

To import this API into Postman:

1. Open Postman
2. Click "Import" → "Link"
3. Enter: `http://localhost:8000/docs` (while API is running)
4. Postman will auto-generate collection from OpenAPI spec

Or use the OpenAPI JSON:
```
http://localhost:8000/openapi.json
```

---

## cURL Examples

### Health Check
```bash
curl -X GET http://localhost:8000/api/v1/health
```

### Model Info
```bash
curl -X GET http://localhost:8000/api/v1/model/info
```

### Predict Price
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

---

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success - Request processed successfully |
| 422 | Validation Error - Invalid input data (see error details) |
| 500 | Internal Server Error - Unexpected error during prediction |
| 503 | Service Unavailable - Model not loaded yet |

---

## Model Performance

The API uses a Random Forest model trained on 99,831 UK property sales with the following performance:

- **R² Score (general):** 11.16%
- **R² Score (properties <£1M):** 27% (covers 98.6% of properties)
- **MAE:** £86,796
- **Training Period:** 1995-2025
- **Features:** 6 (property_type, county, postcode_region, old_new, duration, year)

### Confidence Intervals

The confidence interval represents the range of predictions from individual trees in the Random Forest:
- **min:** 10th percentile (pessimistic estimate)
- **max:** 90th percentile (optimistic estimate)

Narrower intervals indicate more confident predictions.

---

## Rate Limiting

Currently no rate limiting. In production, consider:
- 100 requests/minute per IP
- API key authentication for higher limits

---

## CORS Configuration

Current: Allow all origins (`*`)

In production, update `app/main.py`:
```python
allow_origins=["https://yourdomain.com"]
```

---

## Contact & Support

- **GitHub:** https://github.com/LucasBiason/ml-sales-forecasting
- **API Version:** 1.0.0
- **Last Updated:** October 29, 2025

