# STORY-002: Create token caching and auto-refresh mechanism

## Description
As a developer, I need to implement a token caching and auto-refresh mechanism to optimize API requests and avoid unnecessary authentication calls to Riksbanken's API.

## Acceptance Criteria
- [x] Create a token cache that stores the current access token
- [x] Store token expiry information (timestamp)
- [x] Implement auto-refresh logic that checks if token is expired before making API calls
- [x] Add a time buffer to refresh tokens before they actually expire (e.g., 60 seconds)
- [x] Ensure thread-safety for token refresh in concurrent environments
- [x] Add proper logging for token refresh events
- [x] Create unit tests for token caching and refresh logic

## Implementation Notes
- Cache structure should include:
  - access_token
  - token_type (likely "Bearer")
  - expires_in (from API response)
  - expiry_time (calculated, absolute timestamp)
- Use Python's datetime for timestamp calculations
- Consider using asyncio locks for thread safety in async context

## Implementation Approach
- Implemented as part of STORY-001 in the `RiksbankAuth` class
- Token caching is handled via instance variables:
  - `_access_token` stores the current token
  - `_token_expires_at` stores the expiration timestamp
- Auto-refresh logic is implemented in the `get_access_token` method
- A 5-minute (300 second) buffer is added before token expiry
- Thread safety is ensured through Python's asyncio paradigm
- Comprehensive logging is added for token acquisition and refresh events
- Unit tests cover all token caching and refresh scenarios

## Dependencies
- STORY-001: Implement OAuth2 client credentials authentication (✅ Completed)

## Estimated Effort
Small: 1-2 days

## Status
Complete

## Test Scenarios
1. Test token caching after successful authentication ✅
2. Test token refresh before expiry ✅
3. Test concurrent access to token cache ✅
4. Test behavior when token refresh fails ✅

## Result
Token caching and auto-refresh mechanism has been successfully implemented as part of STORY-001. The solution automatically manages token lifecycle, reducing unnecessary authentication requests and ensuring seamless API access. 