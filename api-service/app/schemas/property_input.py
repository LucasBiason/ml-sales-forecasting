"""
Property input schema for predictions.
"""

from pydantic import BaseModel, Field, field_validator


class PropertyInput(BaseModel):
    """Schema for property price prediction input."""

    property_type: str = Field(
        ...,
        description="Property type: D=Detached, S=Semi-detached, T=Terraced, F=Flat, O=Other",
        pattern="^[DSTFO]$"
    )
    old_new: str = Field(
        ...,
        description="New or existing: Y=New, N=Existing",
        pattern="^[YN]$"
    )
    duration: str = Field(
        ...,
        description="Tenure type: F=Freehold, L=Leasehold, U=Unknown",
        pattern="^[FLU]$"
    )
    county: str = Field(
        ...,
        description="Property county",
        min_length=2,
        max_length=50
    )
    postcode: str = Field(
        ...,
        description="Full postcode (e.g. SW1A 1AA)",
        min_length=5,
        max_length=10
    )
    year: int = Field(
        ...,
        description="Sale year",
        ge=1995,
        le=2030
    )

    @field_validator("postcode")
    @classmethod
    def validate_postcode(cls, v: str) -> str:
        """Validate and normalize postcode."""
        return v.upper().strip()

    @field_validator("county")
    @classmethod
    def validate_county(cls, v: str) -> str:
        """Normalize county."""
        return v.upper().strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "property_type": "T",
                    "old_new": "N",
                    "duration": "F",
                    "county": "GREATER LONDON",
                    "postcode": "SW1A 1AA",
                    "year": 2024
                }
            ]
        }
    }
