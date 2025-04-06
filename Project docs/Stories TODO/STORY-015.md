# STORY-015: Create tool to fetch calendar day information

## Description
As a developer, I need to create an MCP tool that retrieves calendar day information from Riksbanken's SWEA API, so that LLMs can determine business days and holidays for financial analysis.

## Acceptance Criteria
- [ ] Create a new MCP tool function to fetch calendar day information
- [ ] Ensure the tool fetches data from the SWEA API
- [ ] Implement parameters for date range filtering
- [ ] Format the response in a consistent, structured way
- [ ] Include business day status in the response
- [ ] Document the tool with comprehensive docstrings
- [ ] Add proper error handling
- [ ] Create unit tests for the tool
- [ ] Register the tool with the MCP server

## Implementation Notes
- Function name should be `fetch_calendar_days`
- Required parameters:
  - From date (required)
  - To date (optional, default to a reasonable range like 30 days from start)
- Return format should include:
  - List of calendar days, each with:
    - Date
    - Business day status (true/false)
    - Holiday name (if applicable)
  - Summary statistics (count of business days, count of holidays)
- Consider implementing date validation and formatting
- Consider caching calendar data for common date ranges

## Dependencies
- STORY-004: Implement SWEA API integration
- STORY-007: Define core data models for calendar days

## Estimated Effort
Small: 1-2 days

## Status
Planned

## Test Scenarios
1. Test fetching calendar days for a specific date range
2. Test default behavior when to_date is not specified
3. Test handling of invalid date formats
4. Test error handling for API failures
5. Test identification of business days and holidays
6. Test calculation of summary statistics 