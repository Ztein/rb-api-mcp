# STORY-003: Create base API service for Riksbanken

## Description
As a developer, I need to create a base API service that will replace the existing Kolada API service to allow for consistent interaction with Riksbanken's APIs, handling authentication, request formatting, and response parsing.

## Acceptance Criteria
- [x] Create a new base API service module replacing the existing Kolada service
- [x] Implement common request functionality (GET, POST methods)
- [x] Integrate with authentication service from STORY-001 and STORY-002
- [x] Add proper error handling and response validation
- [x] Include detailed logging for all API requests and responses
- [x] Implement retry logic for transient errors
- [x] Create unit tests for the base API service
- [x] Update the config.py file to replace Kolada's BASE_URL with Riksbanken URLs

## Implementation Notes
- Much of this story has already been implemented as part of STORY-001 with the creation of `RiksbankApiClient` in `src/services/riksbank_api.py`
- The existing `fetch_data_from_kolada` function in `src/services/api.py` has been adapted to create a complementary `fetch_data_from_riksbank` function
- New function `fetch_data_from_riksbank` follows similar patterns for API consumption with consistent error handling
- Kept the Kolada API client for backwards compatibility
- Implemented retry logic with exponential backoff for transient errors (HTTP 429, 502, 503, 504, and network errors)
- Added pagination support similar to the Kolada API function

## Implementation Progress
- Completed:
  - Base API service module (`src/services/riksbank_api.py`)
  - GET and POST methods with proper error handling
  - Authentication integration
  - Detailed logging
  - Unit tests
  - Retry logic for transient errors with exponential backoff
  - Migration of existing API pattern with `fetch_data_from_riksbank` function
  - Configuration file already has Riksbanken URLs

## Dependencies
- STORY-001: Implement OAuth2 client credentials authentication (✅ Completed)
- STORY-002: Create token caching and auto-refresh mechanism (✅ Completed)

## Estimated Effort
Small: 1 day (reduced from original estimate since much is already done)

## Status
Completed

## Test Scenarios
1. Test successful API calls to both SWEA and TORA APIs
2. Test error handling for various HTTP status codes
3. Test retry logic for transient errors
4. Test authentication failure scenarios
5. Test response parsing logic 