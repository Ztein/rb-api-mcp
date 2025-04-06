#!/usr/bin/env python3
"""
Example usage of the SWEA API calendar functionality.
This script demonstrates how to use the SWEA API service to retrieve
calendar days and check business days.
"""
import sys
import asyncio
from datetime import datetime, date, timedelta

from src.services.swea_api import swea_api

async def main():
    """
    Demonstrates the SWEA API calendar functionality with various examples.
    """
    print("SWEA API Calendar Days Example", file=sys.stderr)
    print("===============================", file=sys.stderr)
    
    # Example 1: Get calendar days for the current month
    today = date.today()
    first_day = date(today.year, today.month, 1)
    if today.month == 12:
        next_month = date(today.year + 1, 1, 1)
    else:
        next_month = date(today.year, today.month + 1, 1)
    last_day = next_month - timedelta(days=1)
    
    print(f"\nExample 1: Get calendar days for current month ({first_day.strftime('%B %Y')})", file=sys.stderr)
    print("-------------------------------------------------------------", file=sys.stderr)
    
    result1 = await swea_api.get_calendar_days(
        from_date=first_day,
        to_date=last_day
    )
    
    if "error" in result1:
        print(f"Error: {result1['error']}", file=sys.stderr)
    else:
        days = result1.get("values", [])
        print(f"Retrieved {len(days)} days in {first_day.strftime('%B %Y')}", file=sys.stderr)
        
        # Print the first 5 days
        for i, day in enumerate(days[:5]):
            date_str = day.get("date", "N/A")
            is_business = day.get("isBusinessDay", False)
            weekday = day.get("weekday", "N/A")
            print(f"  {date_str}: {weekday} - Business Day: {is_business}", file=sys.stderr)
        
        if len(days) > 5:
            print("  ...", file=sys.stderr)
    
    # Example 2: Check if today is a business day
    print(f"\nExample 2: Check if today ({today.strftime('%Y-%m-%d')}) is a business day", file=sys.stderr)
    print("-------------------------------------------------------------", file=sys.stderr)
    
    is_business = await swea_api.is_business_day(today)
    print(f"Today ({today.strftime('%Y-%m-%d')}) is a business day: {is_business}", file=sys.stderr)
    
    # Example 3: Get the next 5 business days
    print("\nExample 3: Get business days only", file=sys.stderr)
    print("-------------------------------------------------------------", file=sys.stderr)
    
    result3 = await swea_api.get_calendar_days(
        from_date=today,
        to_date=today + timedelta(days=14),
        include_non_business_days=False
    )
    
    if "error" in result3:
        print(f"Error: {result3['error']}", file=sys.stderr)
    else:
        days = result3.get("values", [])
        print(f"Retrieved {len(days)} business days starting from {today.strftime('%Y-%m-%d')}", file=sys.stderr)
        
        for day in days:
            date_str = day.get("date", "N/A")
            weekday = day.get("weekday", "N/A")
            print(f"  {date_str}: {weekday}", file=sys.stderr)

if __name__ == "__main__":
    print("Starting SWEA Calendar API Example", file=sys.stderr)
    
    # Check if required environment variables are set
    import os
    if not os.getenv("RIKSBANK_CLIENT_ID") or not os.getenv("RIKSBANK_CLIENT_SECRET"):
        print("WARNING: RIKSBANK_CLIENT_ID and/or RIKSBANK_CLIENT_SECRET environment variables not set.", file=sys.stderr)
        print("The example will likely fail to authenticate. Set these variables before running.", file=sys.stderr)
        print("You can set them temporarily with:", file=sys.stderr)
        print("  export RIKSBANK_CLIENT_ID=your_client_id", file=sys.stderr)
        print("  export RIKSBANK_CLIENT_SECRET=your_client_secret", file=sys.stderr)
    
    # Run the async main function
    asyncio.run(main())
    
    print("\nSWEA Calendar API Example completed.", file=sys.stderr) 