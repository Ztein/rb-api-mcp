# STORY-012: Create tool to list interest rate types

## Description
As a developer, I need to create an MCP tool that lists available interest rate types from Riksbanken's API, replacing the existing Kolada KPI listing tool, so that LLMs can discover and access relevant financial data.

## Acceptance Criteria
- [x] Create a new MCP tool function to list interest rate types
- [x] Ensure the tool fetches data from the TORA API
- [x] Implement filtering options (e.g., by category, by date range)
- [x] Format the response in a consistent, structured way
- [x] Document the tool with comprehensive docstrings
- [x] Add proper error handling
- [x] Create unit tests for the tool
- [x] Register the tool with the MCP server

## Implementation Notes
- This tool will replace `list_operating_areas` and `get_kpis_by_operating_area` from the Kolada implementation
- Function name should be `list_interest_rate_types`
- Return format should include:
  - Interest rate ID
  - Name/title
  - Brief description
  - Category/type (if applicable)
  - Date range availability
- Consider caching frequently accessed interest rate type data

## Dependencies
- STORY-005: Implement TORA API integration
- STORY-006: Define core data models for interest rates

## Estimated Effort
Small: 1-2 days

## Status
Completed

## Test Scenarios
1. Test listing all available interest rate types
2. Test filtering by category
3. Test filtering by date range
4. Test error handling for API failures
5. Test handling empty results 

## Implementation Approach
1. Created a new `InterestRateType` model in src/models/types.py
2. Added a function in src/tools/riksbank_tools.py to implement the listing functionality
3. Added caching mechanism for interest rate types in the lifespan context
4. Implemented filtering by category and date range
5. Added proper error handling for API failures
6. Added support for cached results to avoid redundant API calls
7. Registered the tool in server.py to make it available via MCP
8. Created comprehensive tests in tests/test_riksbank_tools.py 