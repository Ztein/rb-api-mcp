import json
import sys
import traceback
from typing import Any, Dict, Optional, List

import httpx
from src.services.riksbank_api import riksbank_api


async def fetch_data_from_kolada(url: str) -> dict[str, Any]:
    """
    Helper function to fetch data from Kolada with consistent error handling.
    Now includes pagination support: if 'next_page' is present, we keep fetching
    subsequent pages and merge 'values' into one combined list.
    """
    combined_values: list[dict[str, Any]] = []
    visited_urls: set[str] = set()

    this_url: str | None = url
    async with httpx.AsyncClient() as client:
        while this_url and this_url not in visited_urls:
            visited_urls.add(this_url)
            print(f"[Kolada MCP] Fetching page: {this_url}", file=sys.stderr)
            try:
                resp = await client.get(this_url, timeout=60.0)
                resp.raise_for_status()
                data: dict[str, Any] = resp.json()
            except (
                httpx.RequestError,
                httpx.HTTPStatusError,
                json.JSONDecodeError,
            ) as ex:
                error_msg: str = f"Error accessing Kolada API: {ex}"
                print(f"[Kolada MCP] {error_msg}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return {"error": error_msg, "details": str(ex), "endpoint": this_url}

            if "error" in data:
                return data

            page_values: list[dict[str, Any]] = data.get("values", [])
            combined_values.extend(page_values)

            next_url: str | None = data.get("next_page")
            if not next_url:
                this_url = None
            else:
                this_url = next_url

    return {
        "count": len(combined_values),
        "values": combined_values,
    }


async def fetch_data_from_riksbank(
    endpoint: str,
    api_type: str = "swea",
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Helper function to fetch data from Riksbanken APIs with consistent error handling.
    Supports both SWEA and TORA APIs, with automatic pagination where available.
    
    Args:
        endpoint: API endpoint path without base URL
        api_type: API type to use ('swea' or 'tora')
        method: HTTP method ('GET' or 'POST')
        params: Query parameters for the request
        data: JSON body data for POST requests
        max_retries: Maximum number of retry attempts for transient errors
        
    Returns:
        Dict containing combined response data from all pages or error information
    """
    print(f"[Riksbank MCP] Fetching from {api_type.upper()} API: {endpoint}", file=sys.stderr)
    
    # Use the appropriate method based on the requested HTTP method
    if method.upper() == "GET":
        response = await riksbank_api.get(
            endpoint=endpoint,
            api_type=api_type,
            params=params,
            max_retries=max_retries
        )
    elif method.upper() == "POST":
        if data is None:
            data = {}
        response = await riksbank_api.post(
            endpoint=endpoint,
            api_type=api_type,
            data=data,
            params=params,
            max_retries=max_retries
        )
    else:
        return {
            "error": f"Unsupported HTTP method: {method}",
            "details": "Only GET and POST methods are supported",
            "endpoint": endpoint
        }
    
    # Check for errors in the response
    if "error" in response:
        return response
    
    # Handle pagination if available (similar to Kolada API)
    # Note: This assumes Riksbank API uses a similar pagination approach
    if isinstance(response, dict) and "values" in response:
        combined_values: List[Dict[str, Any]] = response.get("values", [])
        next_page = response.get("next_page")
        
        # If there's a next page, recursively fetch it and combine the results
        if next_page:
            print(f"[Riksbank MCP] Fetching next page: {next_page}", file=sys.stderr)
            # For simplicity, we'll assume next_page is a full URL that needs to be parsed
            # In practice, you may need to adjust this based on Riksbank's API structure
            next_params = params.copy() if params else {}
            next_params.update({"page": next_page})
            
            next_response = await fetch_data_from_riksbank(
                endpoint=endpoint,
                api_type=api_type,
                method=method,
                params=next_params,
                data=data,
                max_retries=max_retries
            )
            
            if "error" not in next_response and "values" in next_response:
                combined_values.extend(next_response.get("values", []))
            
        return {
            "count": len(combined_values),
            "values": combined_values
        }
    
    # If no pagination is used, just return the response as is
    return response
