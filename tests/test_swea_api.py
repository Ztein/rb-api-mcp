import json
from datetime import datetime, date
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from httpx import Response

from src.services.swea_api import SweaApiService, swea_api

@pytest.fixture
def mock_fetch_data():
    """Mock the fetch_data_from_riksbank function used by SweaApiService"""
    with patch("src.services.swea_api.fetch_data_from_riksbank") as mock:
        yield mock

@pytest.fixture
def calendar_days_response():
    """Sample calendar days response from SWEA API"""
    return {
        "count": 3,
        "values": [
            {
                "date": "2023-01-01",
                "isBusinessDay": False,
                "holiday": "New Year's Day"
            },
            {
                "date": "2023-01-02",
                "isBusinessDay": True,
                "holiday": None
            },
            {
                "date": "2023-01-03",
                "isBusinessDay": True,
                "holiday": None
            }
        ]
    }

@pytest.mark.asyncio
async def test_get_calendar_days_string_date(mock_fetch_data, calendar_days_response):
    """Test fetching calendar days with string date format"""
    # Setup the mock
    mock_fetch_data.return_value = calendar_days_response
    
    # Call the method
    result = await swea_api.get_calendar_days(from_date="2023-01-01", to_date="2023-01-03")
    
    # Check the result
    assert result["count"] == 3
    assert len(result["values"]) == 3
    
    # Verify the mock was called correctly
    mock_fetch_data.assert_called_once()
    args, kwargs = mock_fetch_data.call_args
    assert kwargs["endpoint"] == "/calendar/calendardays"
    assert kwargs["api_type"] == "swea"
    assert kwargs["params"]["fromDate"] == "2023-01-01"
    assert kwargs["params"]["toDate"] == "2023-01-03"

@pytest.mark.asyncio
async def test_get_calendar_days_date_object(mock_fetch_data, calendar_days_response):
    """Test fetching calendar days with date objects"""
    # Setup the mock
    mock_fetch_data.return_value = calendar_days_response
    
    # Call the method with date objects
    from_date = date(2023, 1, 1)
    to_date = date(2023, 1, 3)
    result = await swea_api.get_calendar_days(from_date=from_date, to_date=to_date)
    
    # Check the result
    assert result["count"] == 3
    assert len(result["values"]) == 3
    
    # Verify the mock was called correctly with string dates
    mock_fetch_data.assert_called_once()
    args, kwargs = mock_fetch_data.call_args
    assert kwargs["params"]["fromDate"] == "2023-01-01"
    assert kwargs["params"]["toDate"] == "2023-01-03"

@pytest.mark.asyncio
async def test_get_calendar_days_datetime_object(mock_fetch_data, calendar_days_response):
    """Test fetching calendar days with datetime objects"""
    # Setup the mock
    mock_fetch_data.return_value = calendar_days_response
    
    # Call the method with datetime objects
    from_date = datetime(2023, 1, 1, 12, 0, 0)
    to_date = datetime(2023, 1, 3, 12, 0, 0)
    result = await swea_api.get_calendar_days(from_date=from_date, to_date=to_date)
    
    # Check the result
    assert result["count"] == 3
    assert len(result["values"]) == 3
    
    # Verify only the date part was used
    mock_fetch_data.assert_called_once()
    args, kwargs = mock_fetch_data.call_args
    assert kwargs["params"]["fromDate"] == "2023-01-01"
    assert kwargs["params"]["toDate"] == "2023-01-03"

@pytest.mark.asyncio
async def test_get_calendar_days_limit(mock_fetch_data, calendar_days_response):
    """Test fetching calendar days with a limit parameter"""
    # Setup the mock
    mock_fetch_data.return_value = calendar_days_response
    
    # Call the method with a limit
    result = await swea_api.get_calendar_days(from_date="2023-01-01", limit=10)
    
    # Verify the limit was passed correctly
    mock_fetch_data.assert_called_once()
    args, kwargs = mock_fetch_data.call_args
    assert kwargs["params"]["limit"] == 10

@pytest.mark.asyncio
async def test_process_calendar_days_response(calendar_days_response):
    """Test processing the calendar days response with added fields"""
    # Create a test instance
    service = SweaApiService()
    
    # Process the sample response
    processed = service._process_calendar_days_response(calendar_days_response)
    
    # Verify additional fields were added
    assert processed["count"] == 3
    assert len(processed["values"]) == 3
    
    # Check the first day (a Sunday)
    first_day = processed["values"][0]
    assert first_day["date"] == "2023-01-01"
    assert first_day["weekday"] == "Sunday"  # Jan 1, 2023 was a Sunday
    assert first_day["weekday_number"] == 6  # 0=Monday, 6=Sunday in Python
    assert first_day["quarter"] == 1  # Q1
    
    # Check the second day (a Monday)
    second_day = processed["values"][1]
    assert second_day["date"] == "2023-01-02"
    assert second_day["weekday"] == "Monday"
    assert second_day["weekday_number"] == 0

@pytest.mark.asyncio
async def test_get_business_days(mock_fetch_data):
    """Test fetching only business days"""
    # Setup the mock
    mock_fetch_data.return_value = {
        "count": 2,
        "values": [
            {"date": "2023-01-02", "isBusinessDay": True},
            {"date": "2023-01-03", "isBusinessDay": True}
        ]
    }
    
    # Call the business days method
    result = await swea_api.get_business_days(from_date="2023-01-01", to_date="2023-01-03")
    
    # Verify that businessDaysOnly param was set
    mock_fetch_data.assert_called_once()
    args, kwargs = mock_fetch_data.call_args
    assert kwargs["params"].get("businessDaysOnly") is True

@pytest.mark.asyncio
async def test_is_business_day_true(mock_fetch_data):
    """Test checking if a date is a business day (true case)"""
    # Setup the mock
    mock_fetch_data.return_value = {
        "count": 1,
        "values": [
            {"date": "2023-01-02", "isBusinessDay": True}
        ]
    }
    
    # Check a business day
    is_business = await swea_api.is_business_day("2023-01-02")
    assert is_business is True

@pytest.mark.asyncio
async def test_is_business_day_false(mock_fetch_data):
    """Test checking if a date is a business day (false case)"""
    # Setup the mock
    mock_fetch_data.return_value = {
        "count": 1,
        "values": [
            {"date": "2023-01-01", "isBusinessDay": False}
        ]
    }
    
    # Check a non-business day
    is_business = await swea_api.is_business_day("2023-01-01")
    assert is_business is False

@pytest.mark.asyncio
async def test_error_handling(mock_fetch_data):
    """Test error handling in the API service"""
    # Setup mock to return an error
    error_response = {
        "error": "API Error",
        "details": "Connection failed"
    }
    mock_fetch_data.return_value = error_response
    
    # Call the method
    result = await swea_api.get_calendar_days(from_date="2023-01-01")
    
    # Verify the error was returned intact
    assert "error" in result
    assert result["error"] == "API Error"
    assert result["details"] == "Connection failed" 