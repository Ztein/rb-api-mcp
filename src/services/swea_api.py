import json
import sys
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date

from src.services.api import fetch_data_from_riksbank

# Configure logging
logger = logging.getLogger(__name__)

class SweaApiService:
    """
    Service for interacting specifically with Riksbanken's SWEA API.
    Provides access to SWEA-specific endpoints like calendar days.
    """
    
    async def get_calendar_days(
        self,
        from_date: Union[str, date, datetime],
        to_date: Optional[Union[str, date, datetime]] = None,
        limit: Optional[int] = 100,
        include_non_business_days: bool = True,
        cache: bool = True
    ) -> Dict[str, Any]:
        """
        Fetch calendar days from SWEA API with optional date range filtering.
        
        Args:
            from_date: Start date for the range (inclusive) - string format 'YYYY-MM-DD' or date object
            to_date: End date for the range (inclusive) - string format 'YYYY-MM-DD' or date object
            limit: Maximum number of calendar days to return
            include_non_business_days: Whether to include weekends and holidays
            cache: Whether to use cached results if available
            
        Returns:
            Dict containing calendar days data or error information
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
            
        if limit:
            params["limit"] = limit
            
        # Add parameter for including/excluding non-business days if API supports it
        # Note: This might need to be adjusted based on actual SWEA API documentation
        if not include_non_business_days:
            params["businessDaysOnly"] = True
        
        logger.debug(f"Fetching calendar days with params: {params}")
        
        # Make the API request
        response = await fetch_data_from_riksbank(
            endpoint="/calendar/calendardays",
            api_type="swea",
            params=params
        )
        
        # Process the response
        if "error" in response:
            logger.error(f"Error fetching calendar days: {response['error']}")
            return response
        
        # Transform the response if needed to match application data models
        # This will depend on the exact structure of the SWEA API response
        processed_response = self._process_calendar_days_response(response)
        
        return processed_response
    
    def _process_calendar_days_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and transform the raw calendar days API response.
        
        Args:
            response: Raw API response from SWEA API
            
        Returns:
            Processed and transformed response
        """
        # If the response doesn't have values field, return as is
        if not isinstance(response, dict) or "values" not in response:
            return response
        
        # Get the calendar days from the response
        calendar_days = response.get("values", [])
        
        # Example transformation - enhance with business day flags, weekday names, etc.
        # This is just an example and should be adjusted based on actual needs
        processed_days = []
        for day in calendar_days:
            # Clone the day data
            processed_day = day.copy()
            
            # Add additional fields if needed
            if "date" in day:
                try:
                    # Parse the date string
                    day_date = datetime.strptime(day["date"], "%Y-%m-%d")
                    
                    # Add weekday information
                    processed_day["weekday"] = day_date.strftime("%A")
                    processed_day["weekday_number"] = day_date.weekday()
                    
                    # Add quarter information
                    processed_day["quarter"] = (day_date.month - 1) // 3 + 1
                    
                except (ValueError, TypeError):
                    # If date parsing fails, just keep the original data
                    pass
            
            processed_days.append(processed_day)
        
        # Return processed data
        return {
            "count": len(processed_days),
            "values": processed_days
        }
    
    async def get_business_days(
        self,
        from_date: Union[str, date, datetime],
        to_date: Optional[Union[str, date, datetime]] = None,
        limit: Optional[int] = 100
    ) -> Dict[str, Any]:
        """
        Convenience method to fetch only business days.
        
        Args:
            from_date: Start date for the range (inclusive)
            to_date: End date for the range (inclusive)
            limit: Maximum number of calendar days to return
            
        Returns:
            Dict containing only business days
        """
        return await self.get_calendar_days(
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            include_non_business_days=False
        )
    
    async def is_business_day(self, check_date: Union[str, date, datetime]) -> bool:
        """
        Check if a specific date is a business day.
        
        Args:
            check_date: The date to check
            
        Returns:
            True if the date is a business day, False otherwise
        """
        # Convert date object to string format
        if isinstance(check_date, (date, datetime)):
            check_date = check_date.strftime('%Y-%m-%d')
        
        # Fetch the specific date
        response = await self.get_calendar_days(from_date=check_date, to_date=check_date)
        
        # Check for errors
        if "error" in response:
            logger.error(f"Error checking business day: {response['error']}")
            # Default to True in case of error to avoid blocking operations
            return True
        
        # Check if the date is a business day
        calendar_days = response.get("values", [])
        if not calendar_days:
            return False
        
        # The actual field name will depend on the SWEA API response structure
        # This is just an example and should be adjusted
        return calendar_days[0].get("isBusinessDay", True)

# Create a singleton instance
swea_api = SweaApiService() 