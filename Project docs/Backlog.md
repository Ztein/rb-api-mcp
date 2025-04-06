# Riksbanken MCP Server Project Backlog

## Core Features
1. **Authentication Integration** - Implement OAuth2 authentication for Riksbanken APIs
2. **API Integration Layer** - Create a service layer to interact with Riksbanken APIs (SWEA and TORA)
3. **Data Model Transformation** - Create data models that represent Riksbanken data structures
4. **Embedding Creation** - Create and manage embeddings for Riksbanken entities for semantic search
5. **Interest Rate Tools** - Tools for accessing and analyzing Riksbanken interest rate data
6. **Calendar/Business Day Tools** - Tools for accessing calendar day information
7. **Exchange Rate Tools** - Tools for accessing and analyzing currency exchange rates
8. **Visualization Support** - Provide data in formats ready for visualization
9. **Testing Infrastructure** - Create comprehensive testing infrastructure

## Stories
The following sections list all stories, organized by feature. Each story is tracked with its current status.

### Authentication Integration
- ✅ STORY-001: Implement OAuth2 client credentials authentication
- ✅ STORY-002: Create token caching and auto-refresh mechanism

### API Integration Layer
- ✅ STORY-003: Create base API service for Riksbanken
- STORY-004: Implement SWEA API integration
- STORY-005: Implement TORA API integration

### Data Model Transformation
- STORY-006: Define core data models for interest rates
- STORY-007: Define core data models for calendar days
- STORY-008: Define core data models for exchange rates

### Embedding Creation
- STORY-009: Create embedding infrastructure for Riksbanken entities
- STORY-010: Implement semantic search for interest rate types
- STORY-011: Build embedding cache management

### Interest Rate Tools
- STORY-012: Create tool to list interest rate types
- STORY-013: Create tool to fetch specific interest rate data
- STORY-014: Create tool to analyze interest rate trends

### Calendar/Business Day Tools
- STORY-015: Create tool to fetch calendar day information
- STORY-016: Create tool to check if a specific date is a business day

### Exchange Rate Tools
- STORY-017: Create tool to list available currency exchange rates
- STORY-018: Create tool to fetch specific exchange rate data
- STORY-019: Create tool to analyze exchange rate trends

### Visualization Support
- STORY-020: Ensure data is returned in formats suitable for visualization
- STORY-021: Add time series formatting for charting

### Testing Infrastructure
- STORY-022: Create unit test infrastructure
- STORY-023: Implement integration tests with Riksbanken API
- STORY-024: Create mocked responses for tests 