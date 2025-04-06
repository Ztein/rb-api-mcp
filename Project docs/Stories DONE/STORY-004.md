# STORY-004: Implement SWEA API integration

## Description
As a developer, I need to implement specific service functions to interact with Riksbanken's SWEA API, so that the MCP server can access calendar day data and other historical information.

## Acceptance Criteria
- [x] Create SWEA API specific service module
- [x] Implement function to fetch calendar days from SWEA API
- [x] Handle SWEA-specific data formats and responses
- [x] Properly parse and transform SWEA API responses into usable data structures
- [x] Add detailed error handling for SWEA-specific error conditions
- [x] Implement caching for SWEA API responses where appropriate
- [x] Create unit tests for SWEA API integration
- [x] Document all implemented SWEA API endpoints

## Implementation Notes
- Base URL for SWEA API: https://api.riksbank.se/swea/v1
- Key endpoint: /calendar/calendardays
- Review the SWEA API documentation for parameter requirements
- Consider implementing pagination handling for large result sets
- Map SWEA API responses to application data models

## Dependencies
- STORY-003: Create base API service for Riksbanken

## Estimated Effort
Medium: 2-3 days

## Status
Completed

## Start Date
2024-06-30

## Completion Date
2024-06-30

## Implementation Details
- Created `swea_api.py` service with a `SweaApiService` class and singleton instance
- Implemented several calendar day-related functions:
  - `get_calendar_days()` - Main function for fetching calendar days
  - `get_business_days()` - Convenience method for fetching only business days
  - `is_business_day()` - Quick check if a date is a business day
- Added processing logic to enhance API responses with additional fields
- Created comprehensive unit tests in `test_swea_api.py`
- Added tool functions in `riksbank_tools.py` to expose functionality:
  - `get_calendar_days()` - Tool function for calendar days
  - `check_is_business_day()` - Tool function to check business days
  - `get_next_business_days()` - Tool function to get upcoming business days
- Updated entry prompt to include new SWEA calendar functionality
- Created example usage in `examples/swea_calendar_example.py`

## Test Scenarios
1. Test fetching calendar days for a specific date range
2. Test error handling for invalid parameters
3. Test pagination handling for large result sets
4. Test response parsing and transformation 