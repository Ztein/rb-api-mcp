import pytest
from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.tora_api import tora_api

@pytest.mark.asyncio
async def test_get_interest_rates_success():
    """Test successful interest rate data fetching."""
    # Mock response data
    mock_response = {
        "values": [
            {
                "id": "REPO",
                "value": 4.0,
                "date": "2024-03-20",
                "type": "Policy Rate",
                "description": "Repo Rate",
                "unit": "%"
            }
        ]
    }
    
    # Mock the fetch_data_from_riksbank function
    with patch("src.services.tora_api.fetch_data_from_riksbank", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_response
        
        # Test with string date
        result = await tora_api.get_interest_rates("2024-03-20")
        assert result["count"] == 1
        assert result["values"][0]["id"] == "REPO"
        assert result["values"][0]["value"] == 4.0
        
        # Test with date object
        result = await tora_api.get_interest_rates(date(2024, 3, 20))
        assert result["count"] == 1
        
        # Test with datetime object
        result = await tora_api.get_interest_rates(datetime(2024, 3, 20))
        assert result["count"] == 1
        
        # Verify the API was called with correct parameters
        mock_fetch.assert_called_with(
            endpoint="/interestrate",
            api_type="tora",
            params={"fromDate": "2024-03-20"}
        )

@pytest.mark.asyncio
async def test_get_interest_rates_with_filters():
    """Test interest rate data fetching with various filters."""
    mock_response = {"values": []}
    
    with patch("src.services.tora_api.fetch_data_from_riksbank", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_response
        
        # Test with all filters
        result = await tora_api.get_interest_rates(
            from_date="2024-03-01",
            to_date="2024-03-31",
            interest_rate_id="REPO",
            limit=50
        )
        
        # Verify the API was called with all parameters
        mock_fetch.assert_called_with(
            endpoint="/interestrate",
            api_type="tora",
            params={
                "fromDate": "2024-03-01",
                "toDate": "2024-03-31",
                "interestRateId": "REPO",
                "limit": 50
            }
        )

@pytest.mark.asyncio
async def test_get_interest_rates_error_handling():
    """Test error handling in interest rate data fetching."""
    error_response = {
        "error": "Invalid date format",
        "details": "Date must be in YYYY-MM-DD format"
    }
    
    with patch("src.services.tora_api.fetch_data_from_riksbank", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = error_response
        
        result = await tora_api.get_interest_rates("2024-03-20")
        assert "error" in result
        assert result["error"] == "Invalid date format"

@pytest.mark.asyncio
async def test_process_interest_rates_response():
    """Test processing of interest rate response data."""
    # Test with valid response
    valid_response = {
        "values": [
            {
                "id": "REPO",
                "value": 4.0,
                "date": "2024-03-20",
                "type": "Policy Rate",
                "description": "Repo Rate"
            }
        ]
    }
    
    processed = tora_api._process_interest_rates_response(valid_response)
    assert processed["count"] == 1
    assert processed["values"][0]["id"] == "REPO"
    assert processed["values"][0]["unit"] == "%"  # Default unit
    assert processed["values"][0]["source"] == "TORA API"
    
    # Test with invalid response
    invalid_response = {"error": "Invalid response"}
    processed = tora_api._process_interest_rates_response(invalid_response)
    assert processed == invalid_response
    
    # Test with empty response
    empty_response = {"values": []}
    processed = tora_api._process_interest_rates_response(empty_response)
    assert processed["count"] == 0
    assert processed["values"] == [] 