import json
import sys
import logging
import traceback
import asyncio
from typing import Any, Dict, Optional, Union, Callable

import httpx
from src.config import SWEA_BASE_URL, TORA_BASE_URL
from src.services.auth import riksbank_auth

# Configure logging
logger = logging.getLogger(__name__)

class RiksbankApiClient:
    """
    Client for interacting with Riksbanken's APIs (SWEA and TORA).
    Handles authentication and API requests with error handling.
    """
    
    async def request(
        self, 
        method: str, 
        endpoint: str, 
        api_type: str = "swea", 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        retry_on_status_codes: Optional[list[int]] = None,
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to Riksbanken API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path without base URL
            api_type: API type to use ('swea' or 'tora')
            params: Query parameters for the request
            data: JSON body data for POST/PUT requests
            headers: Additional headers to include
            max_retries: Maximum number of retry attempts for transient errors
            retry_delay: Initial delay between retries (seconds), will be increased exponentially
            retry_on_status_codes: HTTP status codes to retry on (default: 429, 502, 503, 504)
            
        Returns:
            Dict containing the response data or error information
        """
        # Set default status codes for retry if none provided
        if retry_on_status_codes is None:
            retry_on_status_codes = [429, 502, 503, 504]  # Rate limit and server errors
            
        # Determine base URL based on API type
        if api_type.lower() == "swea":
            base_url = SWEA_BASE_URL
        elif api_type.lower() == "tora":
            base_url = TORA_BASE_URL
        else:
            logger.error(f"Invalid API type: {api_type}")
            return {"error": f"Invalid API type: {api_type}"}
        
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
            
        url = f"{base_url}{endpoint}"
        
        # Prepare headers with authentication
        if headers is None:
            headers = {}
        
        # Initialize retry counter
        retry_count = 0
        current_delay = retry_delay
        
        while True:
            try:
                # Get access token
                access_token = await riksbank_auth.get_access_token()
                headers["Authorization"] = f"Bearer {access_token}"
                
                # Add content-type header for requests with body
                if data and "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
                    
                logger.debug(f"Making {method} request to {url}")
                
                async with httpx.AsyncClient() as client:
                    response = await client.request(
                        method=method,
                        url=url,
                        params=params,
                        json=data if data else None,
                        headers=headers,
                        timeout=30.0
                    )
                    
                    # Check if we need to retry based on status code
                    if response.status_code in retry_on_status_codes and retry_count < max_retries:
                        retry_count += 1
                        wait_time = current_delay * (2 ** (retry_count - 1))  # Exponential backoff
                        
                        logger.warning(
                            f"Received status {response.status_code}, retrying in {wait_time:.2f}s "
                            f"(attempt {retry_count}/{max_retries})"
                        )
                        
                        await asyncio.sleep(wait_time)
                        continue
                    
                    # If not retrying, raise for status as before
                    response.raise_for_status()
                    return response.json()
                    
            except httpx.RequestError as e:
                # Network errors might be transient, retry if we have attempts left
                if retry_count < max_retries:
                    retry_count += 1
                    wait_time = current_delay * (2 ** (retry_count - 1))
                    
                    logger.warning(
                        f"Network error: {e}, retrying in {wait_time:.2f}s "
                        f"(attempt {retry_count}/{max_retries})"
                    )
                    
                    await asyncio.sleep(wait_time)
                    continue
                
                # If we've exhausted retries or shouldn't retry, return error
                error_msg = f"Network error accessing Riksbank API: {e}"
                logger.error(error_msg)
                return {"error": error_msg, "details": str(e), "endpoint": url}
                
            except httpx.HTTPStatusError as e:
                # For HTTP errors that weren't caught by the retry logic above
                error_msg = f"HTTP error accessing Riksbank API: {e.response.status_code}"
                logger.error(error_msg)
                try:
                    error_data = e.response.json()
                    logger.error(f"Error details: {error_data}")
                    return {"error": error_msg, "details": error_data, "endpoint": url}
                except json.JSONDecodeError:
                    logger.error(f"Error response: {e.response.text}")
                    return {"error": error_msg, "details": e.response.text, "endpoint": url}
                    
            except Exception as e:
                error_msg = f"Unexpected error accessing Riksbank API: {e}"
                logger.error(error_msg)
                traceback.print_exc(file=sys.stderr)
                return {"error": error_msg, "details": str(e), "endpoint": url}
            
            # If we reach here, we've either succeeded or exhausted retries
            break
    
    async def get(
        self, 
        endpoint: str, 
        api_type: str = "swea", 
        params: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Make a GET request to Riksbanken API.
        
        Args:
            endpoint: API endpoint path without base URL
            api_type: API type to use ('swea' or 'tora')
            params: Query parameters for the request
            max_retries: Maximum number of retry attempts for transient errors
            
        Returns:
            Dict containing the response data or error information
        """
        return await self.request("GET", endpoint, api_type, params=params, max_retries=max_retries)
    
    async def post(
        self, 
        endpoint: str, 
        data: Dict[str, Any],
        api_type: str = "swea", 
        params: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Make a POST request to Riksbanken API.
        
        Args:
            endpoint: API endpoint path without base URL
            data: JSON body data
            api_type: API type to use ('swea' or 'tora')
            params: Query parameters for the request
            max_retries: Maximum number of retry attempts for transient errors
            
        Returns:
            Dict containing the response data or error information
        """
        return await self.request("POST", endpoint, api_type, params=params, data=data, max_retries=max_retries)

# Create a singleton instance
riksbank_api = RiksbankApiClient() 