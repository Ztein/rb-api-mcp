from unittest.mock import patch, AsyncMock, MagicMock

import pytest
import httpx
from src.services.riksbank_api import RiksbankApiClient

@pytest.fixture
def api_client():
    """Create a RiksbankApiClient instance for testing."""
    return RiksbankApiClient()

@pytest.mark.asyncio
async def test_request_swea_success(api_client):
    """Test successful request to SWEA API."""
    # Mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test_data"}
    mock_response.raise_for_status = AsyncMock()
    
    # Mock httpx client
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.request.return_value = mock_response
    
    # Mock auth token
    mock_auth = AsyncMock()
    mock_auth.get_access_token.return_value = "test_token"
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        with patch("src.services.riksbank_api.riksbank_auth", mock_auth):
            result = await api_client.request("GET", "/test-endpoint", "swea")
            
            # Verify result
            assert result == {"data": "test_data"}
            
            # Verify token was obtained
            mock_auth.get_access_token.assert_called_once()
            
            # Verify request was made correctly
            mock_client.__aenter__.return_value.request.assert_called_once()
            call_args = mock_client.__aenter__.return_value.request.call_args[1]
            assert call_args["method"] == "GET"
            assert "https://api.riksbank.se/swea/v1/test-endpoint" in call_args["url"]
            assert call_args["headers"]["Authorization"] == "Bearer test_token"

@pytest.mark.asyncio
async def test_request_tora_success(api_client):
    """Test successful request to TORA API."""
    # Mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test_data"}
    mock_response.raise_for_status = AsyncMock()
    
    # Mock httpx client
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.request.return_value = mock_response
    
    # Mock auth token
    mock_auth = AsyncMock()
    mock_auth.get_access_token.return_value = "test_token"
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        with patch("src.services.riksbank_api.riksbank_auth", mock_auth):
            result = await api_client.request("GET", "/test-endpoint", "tora")
            
            # Verify result
            assert result == {"data": "test_data"}
            
            # Verify request was made correctly
            call_args = mock_client.__aenter__.return_value.request.call_args[1]
            assert "https://api.riksbank.se/tora/v1/test-endpoint" in call_args["url"]

@pytest.mark.asyncio
async def test_request_invalid_api_type(api_client):
    """Test request with invalid API type."""
    result = await api_client.request("GET", "/test-endpoint", "invalid")
    
    # Verify error is returned
    assert "error" in result
    assert "Invalid API type: invalid" in result["error"]

@pytest.mark.asyncio
async def test_request_http_error(api_client):
    """Test handling of HTTP errors."""
    # Mock response with error
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_response.json.return_value = {"error": "invalid_token"}
    
    http_error = httpx.HTTPStatusError(
        "401 Unauthorized", 
        request=MagicMock(), 
        response=mock_response
    )
    
    # Mock httpx client
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.request.side_effect = http_error
    
    # Mock auth token
    mock_auth = AsyncMock()
    mock_auth.get_access_token.return_value = "test_token"
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        with patch("src.services.riksbank_api.riksbank_auth", mock_auth):
            result = await api_client.request("GET", "/test-endpoint", "swea")
            
            # Verify error details
            assert "error" in result
            assert "HTTP error" in result["error"]
            assert result["details"] == {"error": "invalid_token"}

@pytest.mark.asyncio
async def test_request_network_error(api_client):
    """Test handling of network errors."""
    # Create RequestError
    request_error = httpx.RequestError("Connection error", request=MagicMock())
    
    # Mock httpx client
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.request.side_effect = request_error
    
    # Mock auth token
    mock_auth = AsyncMock()
    mock_auth.get_access_token.return_value = "test_token"
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        with patch("src.services.riksbank_api.riksbank_auth", mock_auth):
            result = await api_client.request("GET", "/test-endpoint", "swea")
            
            # Verify error details
            assert "error" in result
            assert "Network error" in result["error"]
            assert "Connection error" in result["details"]

@pytest.mark.asyncio
async def test_get_method(api_client):
    """Test the get convenience method."""
    # Mock the request method
    api_client.request = AsyncMock()
    api_client.request.return_value = {"data": "test_data"}
    
    result = await api_client.get("/test", "swea", {"param": "value"})
    
    # Verify request was called with correct arguments
    api_client.request.assert_called_once_with(
        "GET", "/test", "swea", params={"param": "value"}
    )
    assert result == {"data": "test_data"}

@pytest.mark.asyncio
async def test_post_method(api_client):
    """Test the post convenience method."""
    # Mock the request method
    api_client.request = AsyncMock()
    api_client.request.return_value = {"data": "test_data"}
    
    data = {"test": "data"}
    result = await api_client.post("/test", data, "swea", {"param": "value"})
    
    # Verify request was called with correct arguments
    api_client.request.assert_called_once_with(
        "POST", "/test", "swea", params={"param": "value"}, data=data
    )
    assert result == {"data": "test_data"} 