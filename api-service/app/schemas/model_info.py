"""
Model information schema.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ModelInfoResponse(BaseModel):
    """Detailed model information schema."""

    loaded: bool = Field(..., description="Whether model is loaded")
    model_type: Optional[str] = Field(None, description="Model type")
    n_estimators: Optional[int] = Field(None, description="Number of estimators")
    features: Optional[List[str]] = Field(None, description="Features used")
    training_samples: Optional[int] = Field(None, description="Training samples count")
    cv_r2_mean: Optional[float] = Field(
        None, description="Mean R2 from cross-validation"
    )
    expected_r2: Optional[float] = Field(None, description="Expected R2 score")
    trained_date: Optional[str] = Field(None, description="Training date")
