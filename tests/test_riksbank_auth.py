import json
import os
import time
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
import httpx
from src.services.auth import RiksbankAuth

@pytest.fixture
def mock_env_vars():
    """Set up mock environment variables for testing."""
    with patch.dict(os.environ, {
        "RIKSBANK_CLIENT_ID": "test_client_id",
        "RIKSBANK_CLIENT_SECRET": "test_client_secret"
    }):
        yield

@pytest.fixture
def auth_instance(mock_env_vars):
    """Create a RiksbankAuth instance with mock environment variables."""
    return RiksbankAuth()

@pytest.mark.asyncio
async def test_init_with_missing_credentials():
    """Test that RiksbankAuth logs a warning when credentials are missing but doesn't fail."""
    with patch.dict(os.environ, {}, clear=True):
        with patch("src.services.auth.logger") as mock_logger:
            auth = RiksbankAuth()
            # Verify warning was logged
            mock_logger.warning.assert_called_once()
            assert "Riksbank API credentials not found" in mock_logger.warning.call_args[0][0]
            
            # Test that get_access_token raises ValueError when called
            with pytest.raises(ValueError, match="Missing Riksbank API credentials"):
                await auth.get_access_token()

@pytest.mark.asyncio
async def test_fetch_new_token_success(auth_instance):
    """Test that _fetch_new_token successfully obtains a token."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "access_token": "test_access_token",
        "expires_in": 3600
    }
    mock_response.raise_for_status = AsyncMock()
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.post.return_value = mock_response
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        await auth_instance._fetch_new_token()
        
        # Verify token was set
        assert auth_instance._access_token == "test_access_token"
        # Verify expiry time was set (with 5-minute buffer)
        assert auth_instance._token_expires_at <= time.time() + 3600 - 300
        assert auth_instance._token_expires_at > time.time() + 3600 - 310  # Allow small timing variations

@pytest.mark.asyncio
async def test_fetch_new_token_http_error(auth_instance):
    """Test that _fetch_new_token handles HTTP errors correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_response.json.side_effect = json.JSONDecodeError("", "", 0)
    
    http_error = httpx.HTTPStatusError(
        "401 Unauthorized", 
        request=MagicMock(), 
        response=mock_response
    )
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.post.side_effect = http_error
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(httpx.HTTPStatusError):
            await auth_instance._fetch_new_token()

@pytest.mark.asyncio
async def test_fetch_new_token_request_error(auth_instance):
    """Test that _fetch_new_token handles network errors correctly."""
    request_error = httpx.RequestError("Connection error", request=MagicMock())
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.post.side_effect = request_error
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(httpx.RequestError):
            await auth_instance._fetch_new_token()

@pytest.mark.asyncio
async def test_get_access_token_new_token(auth_instance):
    """Test that get_access_token fetches a new token when none exists."""
    # Mock the _fetch_new_token method
    auth_instance._fetch_new_token = AsyncMock()
    auth_instance._access_token = None
    
    await auth_instance.get_access_token()
    
    # Verify _fetch_new_token was called
    auth_instance._fetch_new_token.assert_called_once()

@pytest.mark.asyncio
async def test_get_access_token_expired_token(auth_instance):
    """Test that get_access_token fetches a new token when the existing one is expired."""
    # Mock the _fetch_new_token method
    auth_instance._fetch_new_token = AsyncMock()
    auth_instance._access_token = "old_token"
    auth_instance._token_expires_at = time.time() - 60  # Expired 1 minute ago
    
    await auth_instance.get_access_token()
    
    # Verify _fetch_new_token was called
    auth_instance._fetch_new_token.assert_called_once()

@pytest.mark.asyncio
async def test_get_access_token_valid_token(auth_instance):
    """Test that get_access_token uses existing token when it's still valid."""
    # Mock the _fetch_new_token method
    auth_instance._fetch_new_token = AsyncMock()
    auth_instance._access_token = "valid_token"
    auth_instance._token_expires_at = time.time() + 3600  # Valid for 1 hour
    
    token = await auth_instance.get_access_token()
    
    # Verify _fetch_new_token was NOT called
    auth_instance._fetch_new_token.assert_not_called()
    # Verify the correct token was returned
    assert token == "valid_token" 