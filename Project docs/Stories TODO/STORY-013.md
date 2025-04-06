# STORY-013: Create tool to fetch specific interest rate data

## Description
As a developer, I need to create an MCP tool that retrieves specific interest rate data from Riksbanken's API, replacing the existing Kolada data fetching tool, so that LLMs can access detailed financial information.

## Acceptance Criteria
- [ ] Create a new MCP tool function to fetch specific interest rate data
- [ ] Ensure the tool fetches data from the TORA API
- [ ] Implement parameters for interest rate ID, date range, and other filters
- [ ] Format the response in a consistent, structured way, including time series data
- [ ] Document the tool with comprehensive docstrings
- [ ] Add proper error handling
- [ ] Create unit tests for the tool
- [ ] Register the tool with the MCP server

## Implementation Notes
- This tool will replace `fetch_kolada_data` from the Kolada implementation
- Function name should be `fetch_interest_rate_data`
- Required parameters:
  - Interest rate ID (from `list_interest_rate_types`)
  - From date (optional, default to recent period)
  - To date (optional, default to most recent data)
- Return format should include:
  - Interest rate metadata (ID, name, description)
  - Time series data points, each with:
    - Date
    - Value
    - Status (if applicable)
  - Summary statistics (latest value, average, min, max)
- Consider implementing data caching for frequently accessed interest rates

## Dependencies
- STORY-005: Implement TORA API integration
- STORY-006: Define core data models for interest rates

## Estimated Effort
Medium: 2-3 days

## Status
Planned

## Test Scenarios
1. Test fetching data for a specific interest rate and date range
2. Test default behavior when dates are not specified
3. Test handling of invalid interest rate IDs
4. Test error handling for API failures
5. Test format of time series data
6. Test calculation of summary statistics 