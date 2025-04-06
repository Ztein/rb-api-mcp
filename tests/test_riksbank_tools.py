import json
from typing import Any, Dict, List, cast
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.models.types import InterestRateType
from tools.riksbank_tools import list_interest_rate_types


@pytest.fixture
def mock_context():
    """Fixture for a mock MCP context."""
    mock_ctx = MagicMock()
    lifespan_context = {}
    mock_ctx.request_context = MagicMock()
    mock_ctx.request_context.lifespan_context = lifespan_context
    return mock_ctx


@pytest.fixture
def interest_rate_types_sample() -> List[InterestRateType]:
    """Sample interest rate types data for testing."""
    return [
        {
            "id": "REPO",
            "name": "Repo rate",
            "description": "The Riksbank's policy rate",
            "category": "Policy Rate",
            "date_range": {
                "from": "1995-01-01",
                "to": "2023-12-31"
            }
        },
        {
            "id": "STIBOR1M",
            "name": "STIBOR 1 month",
            "description": "Stockholm Interbank Offered Rate, 1 month",
            "category": "Money Market",
            "date_range": {
                "from": "2000-01-01",
                "to": "2023-12-31"
            }
        },
        {
            "id": "STIBOR3M",
            "name": "STIBOR 3 months",
            "description": "Stockholm Interbank Offered Rate, 3 months",
            "category": "Money Market",
            "date_range": {
                "from": "2000-01-01",
                "to": "2023-12-31"
            }
        },
        {
            "id": "GOVBOND10Y",
            "name": "Government bond 10Y",
            "description": "Swedish government bond, 10 year maturity",
            "category": "Bond Market",
            "date_range": {
                "from": "1990-01-01",
                "to": "2023-12-31"
            }
        }
    ]


@pytest.mark.asyncio
async def test_list_interest_rate_types_cached(mock_context, interest_rate_types_sample):
    """Test listing interest rate types when they're available in cache."""
    # Set up mock context with cached data
    mock_context.request_context.lifespan_context = {
        "interest_rate_types_cache": interest_rate_types_sample
    }
    
    # Test full list (no filters)
    result = await list_interest_rate_types(mock_context)
    assert len(result) == 4
    assert result[0]["id"] == "REPO"
    
    # Test filtering by category
    result = await list_interest_rate_types(mock_context, category="Money Market")
    assert len(result) == 2
    assert all(item["category"] == "Money Market" for item in result)
    
    # Test filtering by date range (all items should match)
    result = await list_interest_rate_types(
        mock_context, 
        date_from="2020-01-01", 
        date_to="2022-12-31"
    )
    assert len(result) == 4
    
    # Test filtering by date range (only some should match)
    result = await list_interest_rate_types(
        mock_context, 
        date_from="1992-01-01", 
        date_to="1999-12-31"
    )
    assert len(result) == 2  # Both REPO (from 1995) and GOVBOND10Y (from 1990) match
    assert any(item["id"] == "REPO" for item in result)
    assert any(item["id"] == "GOVBOND10Y" for item in result)


@pytest.mark.asyncio
@patch("tools.riksbank_tools.riksbank_api.get")
async def test_list_interest_rate_types_api(mock_get, mock_context):
    """Test listing interest rate types when fetching from API."""
    # Set up mock API response
    mock_api_response = {
        "items": [
            {
                "id": "REPO",
                "name": "Repo rate",
                "description": "The Riksbank's policy rate",
                "category": "Policy Rate",
                "availableFrom": "1995-01-01",
                "availableTo": "2023-12-31"
            },
            {
                "id": "STIBOR3M",
                "name": "STIBOR 3 months",
                "description": "Stockholm Interbank Offered Rate, 3 months",
                "category": "Money Market",
                "availableFrom": "2000-01-01",
                "availableTo": "2023-12-31"
            }
        ]
    }
    
    mock_get.return_value = mock_api_response
    
    # Test API fetch with no filters
    result = await list_interest_rate_types(mock_context)
    
    # Verify API was called with correct params
    mock_get.assert_called_once_with(
        "/interest-rates/types", 
        api_type="tora", 
        params={}
    )
    
    # Verify result
    assert len(result) == 2
    assert result[0]["id"] == "REPO"
    assert result[0]["date_range"]["from"] == "1995-01-01"
    assert result[1]["category"] == "Money Market"


@pytest.mark.asyncio
@patch("tools.riksbank_tools.riksbank_api.get")
async def test_list_interest_rate_types_with_filters(mock_get, mock_context):
    """Test listing interest rate types with filters from API."""
    # Set up mock API response
    mock_api_response = {
        "items": [
            {
                "id": "STIBOR3M",
                "name": "STIBOR 3 months",
                "description": "Stockholm Interbank Offered Rate, 3 months",
                "category": "Money Market",
                "availableFrom": "2000-01-01",
                "availableTo": "2023-12-31"
            }
        ]
    }
    
    mock_get.return_value = mock_api_response
    
    # Test API fetch with filters
    result = await list_interest_rate_types(
        mock_context,
        category="Money Market",
        date_from="2020-01-01",
        date_to="2022-12-31"
    )
    
    # Verify API was called with correct params
    mock_get.assert_called_once_with(
        "/interest-rates/types", 
        api_type="tora", 
        params={
            "category": "Money Market",
            "from": "2020-01-01",
            "to": "2022-12-31"
        }
    )
    
    # Verify result
    assert len(result) == 1
    assert result[0]["id"] == "STIBOR3M"
    
    # Verify data was NOT cached (since we used filters)
    assert "interest_rate_types_cache" not in mock_context.request_context.lifespan_context


@pytest.mark.asyncio
@patch("tools.riksbank_tools.riksbank_api.get")
async def test_list_interest_rate_types_error(mock_get, mock_context):
    """Test error handling when API returns an error."""
    # Set up mock API error response
    mock_get.return_value = {"error": "API error occurred"}
    
    # Test API fetch with error
    result = await list_interest_rate_types(mock_context)
    
    # Verify result is empty list
    assert result == []
    
    # Verify data was NOT cached
    assert "interest_rate_types_cache" not in mock_context.request_context.lifespan_context 