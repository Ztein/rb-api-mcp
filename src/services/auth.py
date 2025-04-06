import os
import time
import logging
from typing import Dict, Optional, Any
import json

import httpx
from src.config import RIKSBANK_TOKEN_URL

# Configure logging
logger = logging.getLogger(__name__)
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level))

class RiksbankAuth:
    """
    Handles OAuth2 client credentials flow authentication for Riksbanken APIs.
    Manages token lifecycle including obtaining and refreshing access tokens.
    """
    def __init__(self):
        self._client_id = os.getenv("RIKSBANK_CLIENT_ID")
        self._client_secret = os.getenv("RIKSBANK_CLIENT_SECRET")
        self._access_token = None
        self._token_expires_at = 0
        
        # Log a warning if credentials are not set, but don't fail initialization
        if not self._client_id or not self._client_secret:
            logger.warning(
                "Riksbank API credentials not found in environment variables. "
                "Authentication will fail when used."
            )
    
    async def get_access_token(self) -> str:
        """
        Returns a valid access token, obtaining a new one if necessary.
        
        Returns:
            str: A valid access token for Riksbanken API
            
        Raises:
            ValueError: If the API credentials are not configured
        """
        # Validate credentials before attempting to get a token
        if not self._client_id or not self._client_secret:
            logger.error("Riksbank API credentials not found in environment variables")
            raise ValueError(
                "Missing Riksbank API credentials. "
                "Please set RIKSBANK_CLIENT_ID and RIKSBANK_CLIENT_SECRET environment variables."
            )
            
        # Check if we need a new token
        current_time = time.time()
        if not self._access_token or current_time >= self._token_expires_at:
            await self._fetch_new_token()
            
        return self._access_token
    
    async def _fetch_new_token(self) -> None:
        """
        Fetches a new access token using client credentials flow.
        
        Raises:
            httpx.RequestError: If there's a network error
            httpx.HTTPStatusError: If the server returns an error status code
            ValueError: If the token response is invalid
        """
        logger.debug("Fetching new access token from Riksbanken")
        
        data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    RIKSBANK_TOKEN_URL, 
                    data=data,
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                token_data = response.json()
                
                # Extract token data
                self._access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)  # Default to 1 hour if not specified
                
                if not self._access_token:
                    logger.error(f"Invalid token response: {token_data}")
                    raise ValueError("Invalid token response from Riksbanken API")
                
                # Set expiry time with a 5-minute buffer
                self._token_expires_at = time.time() + expires_in - 300
                
                logger.info("Successfully obtained new Riksbanken API access token")
                logger.debug(f"Token expires in {expires_in} seconds")
                
        except httpx.RequestError as e:
            logger.error(f"Network error when requesting access token: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error when requesting access token: {e.response.status_code}")
            try:
                error_data = e.response.json()
                logger.error(f"Error details: {error_data}")
            except json.JSONDecodeError:
                logger.error(f"Error response: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error obtaining access token: {e}")
            raise

# Create a singleton instance
riksbank_auth = RiksbankAuth() 