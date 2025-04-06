import sys
from typing import Optional, Dict, Any, List

from mcp.server.fastmcp.server import Context

from src.models.types import InterestRateType
from src.services.riksbank_api import riksbank_api
from src.utils.context import safe_get_lifespan_context


async def list_interest_rate_types(
    ctx: Context,  # type: ignore[Context]
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> List[InterestRateType]:
    """
    **Purpose:** Lists available interest rate types from Riksbanken's TORA API.
    This tool helps discover and understand what interest rate data is available 
    before requesting specific time series data.
    
    **Use Cases:**
    * "What interest rate types are available from Riksbanken?"
    * "Show me policy rates available in the TORA API."
    * "List interest rates available for 2022."
    * "What categories of interest rates can I query?"
    
    **Arguments:**
    * `category` (Optional[str]): Filter interest rates by category (e.g., "Policy Rate", "Money Market").
    * `date_from` (Optional[str]): Filter for interest rates available from this date (format: YYYY-MM-DD).
    * `date_to` (Optional[str]): Filter for interest rates available until this date (format: YYYY-MM-DD).
    * `ctx` (Context): The server context (automatically injected by the MCP framework).
    
    **Return Value:**
    * A list of `InterestRateType` objects containing metadata about each interest rate series.
    * Each object includes id, name, description, category, and date_range information.
    * Returns an empty list if no interest rates match the filter criteria or if an error occurs.
    
    **Notes:**
    * This tool replaces the Kolada `list_operating_areas` and `get_kpis_by_operating_area` tools.
    * Interest rate data can be further queried with other tools once you've identified the right ID.
    """
    
    # Check if we have cached data in the lifespan context
    lifespan_ctx = safe_get_lifespan_context(ctx)
    cached_data = []
    
    if lifespan_ctx and "interest_rate_types_cache" in lifespan_ctx:
        cached_data = lifespan_ctx.get("interest_rate_types_cache", [])
        print(f"[Riksbank Tools] Using cached interest rate types: {len(cached_data)} items", file=sys.stderr)
    
    # If we have cached data, filter it based on the parameters
    if cached_data:
        result = cached_data
        
        # Apply filters if provided
        if category:
            result = [r for r in result if r.get("category", "").lower() == category.lower()]
        
        if date_from or date_to:
            filtered_by_date = []
            for rate in result:
                date_range = rate.get("date_range", {})
                range_from = date_range.get("from", "1900-01-01")
                range_to = date_range.get("to", "2100-12-31")
                
                # Check if date ranges overlap
                if date_from and date_to:
                    if range_from <= date_to and range_to >= date_from:
                        filtered_by_date.append(rate)
                elif date_from:
                    if range_to >= date_from:
                        filtered_by_date.append(rate)
                elif date_to:
                    if range_from <= date_to:
                        filtered_by_date.append(rate)
            
            result = filtered_by_date
            
        return result
    
    # If no cached data, fetch from the API
    try:
        print("[Riksbank Tools] Fetching interest rate types from TORA API", file=sys.stderr)
        
        # Construct API parameters based on filters
        params: Dict[str, Any] = {}
        if category:
            params["category"] = category
        if date_from:
            params["from"] = date_from
        if date_to:
            params["to"] = date_to
            
        # Call the TORA API endpoint for interest rate types
        response = await riksbank_api.get("/interest-rates/types", api_type="tora", params=params)
        
        if "error" in response:
            print(f"[Riksbank Tools] Error fetching interest rate types: {response['error']}", file=sys.stderr)
            return []
            
        # Transform API response into our InterestRateType model
        interest_rates: List[InterestRateType] = []
        
        for item in response.get("items", []):
            interest_rate: InterestRateType = {
                "id": item.get("id", ""),
                "name": item.get("name", ""),
                "description": item.get("description", ""),
                "category": item.get("category", ""),
                "date_range": {
                    "from": item.get("availableFrom", ""),
                    "to": item.get("availableTo", "")
                }
            }
            interest_rates.append(interest_rate)
            
        # Cache the results in lifespan context if possible
        if lifespan_ctx and not category and not date_from and not date_to:
            lifespan_ctx["interest_rate_types_cache"] = interest_rates
            print(f"[Riksbank Tools] Cached {len(interest_rates)} interest rate types", file=sys.stderr)
            
        return interest_rates
        
    except Exception as e:
        print(f"[Riksbank Tools] Unexpected error: {e}", file=sys.stderr)
        return [] 