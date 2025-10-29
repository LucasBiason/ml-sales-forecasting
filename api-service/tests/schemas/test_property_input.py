"""
Unit tests for PropertyInput schema validation.
"""

import pytest
from pydantic import ValidationError

from app.schemas.property_input import PropertyInput


def test_valid_property_input():
    """Test valid property input."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    input_obj = PropertyInput(**data)

    assert input_obj.property_type == "T"
    assert input_obj.old_new == "N"
    assert input_obj.duration == "F"
    assert input_obj.county == "GREATER LONDON"
    assert input_obj.postcode == "SW1A 1AA"
    assert input_obj.year == 2024


def test_invalid_property_type():
    """Test invalid property type."""
    data = {
        "property_type": "X",  # Invalid
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    with pytest.raises(ValidationError) as exc_info:
        PropertyInput(**data)

    assert "property_type" in str(exc_info.value)


def test_valid_property_types():
    """Test all valid property types."""
    valid_types = ["D", "S", "T", "F", "O"]

    for prop_type in valid_types:
        data = {
            "property_type": prop_type,
            "old_new": "N",
            "duration": "F",
            "county": "GREATER LONDON",
            "postcode": "SW1A 1AA",
            "year": 2024,
        }

        input_obj = PropertyInput(**data)
        assert input_obj.property_type == prop_type


def test_invalid_old_new():
    """Test invalid old_new value."""
    data = {
        "property_type": "T",
        "old_new": "X",  # Invalid: must be Y or N
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_invalid_duration():
    """Test invalid duration value."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "X",  # Invalid: must be F, L or U
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_county_too_short():
    """Test county with less than 2 characters."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "A",  # Too short
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_county_too_long():
    """Test county with more than 50 characters."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "A" * 51,  # Too long
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_postcode_too_short():
    """Test postcode with less than 5 characters."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1",  # Too short
        "year": 2024,
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_postcode_too_long():
    """Test postcode with more than 10 characters."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA EXTRA",  # Too long
        "year": 2024,
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_year_below_minimum():
    """Test year below 1995."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 1990,  # Below minimum
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_year_above_maximum():
    """Test year above 2030."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2040,  # Above maximum
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)


def test_postcode_normalization():
    """Test postcode normalization (uppercase and trim)."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "  sw1a 1aa  ",  # Lowercase with spaces
        "year": 2024,
    }

    input_obj = PropertyInput(**data)

    assert input_obj.postcode == "SW1A 1AA"  # Normalized


def test_county_normalization():
    """Test county normalization (uppercase and trim)."""
    data = {
        "property_type": "T",
        "old_new": "N",
        "duration": "F",
        "county": "  greater london  ",  # Lowercase with spaces
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    input_obj = PropertyInput(**data)

    assert input_obj.county == "GREATER LONDON"  # Normalized


def test_missing_required_field():
    """Test missing required field."""
    data = {
        "property_type": "T",
        # Missing old_new
        "duration": "F",
        "county": "GREATER LONDON",
        "postcode": "SW1A 1AA",
        "year": 2024,
    }

    with pytest.raises(ValidationError):
        PropertyInput(**data)
