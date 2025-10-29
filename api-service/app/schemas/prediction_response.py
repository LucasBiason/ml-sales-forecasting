"""
Prediction response schemas.
"""

from pydantic import BaseModel, Field
from typing import List


class ConfidenceInterval(BaseModel):
    """Prediction confidence interval."""

    min: float = Field(..., description="Minimum price (10th percentile)")
    max: float = Field(..., description="Maximum price (90th percentile)")


class ModelInfo(BaseModel):
    """Model information."""

    type: str = Field(..., description="Model type")
    n_estimators: int = Field(..., description="Number of trees")
    expected_r2: float = Field(..., description="Expected R2 score")


class PredictionResponse(BaseModel):
    """Prediction response schema."""

    predicted_price: float = Field(..., description="Predicted price in £")
    confidence_interval: ConfidenceInterval = Field(..., description="Confidence interval")
    features_used: List[str] = Field(..., description="Features used in the model")
    model_info: ModelInfo = Field(..., description="Model information")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "predicted_price": 425000.50,
                    "confidence_interval": {
                        "min": 380000.00,
                        "max": 470000.00
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
                        "expected_r2": 0.11
                    }
                }
            ]
        }
    }
