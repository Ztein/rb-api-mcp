# STORY-025: Add tests for fetch_data_from_riksbank function

## Description
As a developer, I need comprehensive tests for the `fetch_data_from_riksbank` function to ensure it correctly interacts with Riksbanken APIs, handles errors properly, and correctly processes paginated data.

## Acceptance Criteria
- [ ] Create unit tests for `fetch_data_from_riksbank` that test:
  - Successful GET requests
  - Successful POST requests
  - Error handling for HTTP errors
  - Error handling for network errors
  - Handling of paginated responses
  - Parameter passing to the underlying API client
- [ ] Ensure test coverage for all code paths in the function
- [ ] Use proper mocking to avoid actual API calls during tests
- [ ] Verify the function correctly handles both SWEA and TORA API types
- [ ] Verify the function correctly processes and combines paginated data

## Implementation Notes
- The `fetch_data_from_riksbank` function was implemented as part of STORY-003
- The function is located in `src/services/api.py` 
- Similar tests exist for the underlying `RiksbankApiClient` in `tests/test_riksbank_api.py`
- Tests should verify that pagination handling works correctly
- Consider testing edge cases like empty responses or malformed data

## Dependencies
- STORY-003: Create base API service for Riksbanken (✅ Completed)

## Estimated Effort
Small: 1 day

## Status
To Do

## Test Scenarios
1. Test successful GET request with single page response
2. Test successful GET request with multiple page response
3. Test successful POST request
4. Test error handling for HTTP errors
5. Test error handling for network errors
6. Test with both SWEA and TORA API types
7. Test with different parameter combinations 