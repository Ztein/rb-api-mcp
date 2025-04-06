import json
import sys
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date

from src.services.api import fetch_data_from_riksbank
from src.models.types import InterestRateType

# Configure logging
logger = logging.getLogger(__name__)

class ToraApiService:
    """
    Service for interacting specifically with Riksbanken's TORA API.
    Provides access to TORA-specific endpoints like interest rates.
    """
    
    async def get_interest_rates(
        self,
        from_date: Union[str, date, datetime],
        to_date: Optional[Union[str, date, datetime]] = None,
        interest_rate_id: Optional[str] = None,
        limit: Optional[int] = 100,
        cache: bool = True
    ) -> Dict[str, Any]:
        """
        Fetch interest rate data from TORA API with optional filtering.
        
        Args:
            from_date: Start date for the range (inclusive) - string format 'YYYY-MM-DD' or date object
            to_date: End date for the range (inclusive) - string format 'YYYY-MM-DD' or date object
            interest_rate_id: Specific interest rate ID to fetch
            limit: Maximum number of records to return
            cache: Whether to use cached results if available
            
        Returns:
            Dict containing interest rate data or error information
        """
        # Convert date objects to string format
        if isinstance(from_date, (date, datetime)):
            from_date = from_date.strftime('%Y-%m-%d')
        
        if to_date is not None and isinstance(to_date, (date, datetime)):
            to_date = to_date.strftime('%Y-%m-%d')
        
        # Prepare query parameters
        params: Dict[str, Any] = {
            "fromDate": from_date,
        }
        
        if to_date:
            params["toDate"] = to_date
            
        if interest_rate_id:
            params["interestRateId"] = interest_rate_id
            
        if limit:
            params["limit"] = limit
        
        logger.debug(f"Fetching interest rates with params: {params}")
        
        # Make the API request
        response = await fetch_data_from_riksbank(
            endpoint="/interestrate",
            api_type="tora",
            params=params
        )
        
        # Process the response
        if "error" in response:
            logger.error(f"Error fetching interest rates: {response['error']}")
            return response
        
        # Transform the response to match application data models
        processed_response = self._process_interest_rates_response(response)
        
        return processed_response
    
    def _process_interest_rates_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and transform the raw interest rates API response.
        
        Args:
            response: Raw API response from TORA API
            
        Returns:
            Processed and transformed response
        """
        # If the response doesn't have values field, return as is
        if not isinstance(response, dict) or "values" not in response:
            return response
        
        # Get the interest rates from the response
        interest_rates = response.get("values", [])
        
        # Transform each interest rate entry
        processed_rates = []
        for rate in interest_rates:
            processed_rate = {
                "id": rate.get("id"),
                "value": rate.get("value"),
                "date": rate.get("date"),
                "type": rate.get("type"),
                "description": rate.get("description"),
                "unit": rate.get("unit", "%"),  # Default to percentage if not specified
                "source": "TORA API"
            }
            processed_rates.append(processed_rate)
        
        return {
            "count": len(processed_rates),
            "values": processed_rates
        }

# Create a singleton instance
tora_api = ToraApiService() 