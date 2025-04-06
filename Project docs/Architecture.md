# Riksbanken MCP Server Architecture

## Overview
This document outlines the architecture for transforming the Kolada MCP Server into a Riksbanken MCP Server. The primary goal is to provide LLMs with access to Sweden's central bank (Riksbanken) financial data through a similar interface while making necessary adaptations for the new API.

## System Components

### Core Components
1. **MCP Server Layer** - FastMCP implementation to handle LLM requests
2. **API Integration Layer** - Handles authentication and data fetching from Riksbanken APIs
3. **Data Processing Layer** - Processes raw Riksbanken data into structured formats
4. **Tools Layer** - Exposes functionality to LLMs through MCP tooling
5. **Embedding/Search Layer** - Provides semantic search over Riksbanken data entities

### Riksbanken APIs
We will integrate with two primary Riksbanken APIs:
1. **SWEA API** - Sveriges Riksbanks statistik- och dataAPI for calendar days and historical data
   - Base URL: https://api.riksbank.se/swea/v1
   - Primary endpoints: calendar/calendardays

2. **TORA API** - Riksbankens API for interest rates and financial market data
   - Base URL: https://api.riksbank.se/tora/v1
   - Primary endpoints: interestrate

### Data Models

#### Core Entities:
1. **Interest Rates** - Different types of interest rates maintained by Riksbanken
   - Policy rate (Reporänta)
   - Deposit rate (Inlåningsränta)
   - Lending rate (Utlåningsränta)
   - Reference rates (Referensräntor)
   - Exchange rates (Valutakurser)

2. **Calendar Days** - Information about calendar days, including whether they are business days

3. **Authentication Credentials** - OAuth2 client credentials for API access

## API Endpoints & Authentication

### Authentication Flow
- Implement OAuth 2.0 Client Credentials flow
- Cache tokens with expiry tracking
- Auto-refresh expired tokens

### Endpoints to be Implemented
1. **Interest Rate Data** - Fetch interest rate data
2. **Calendar Data** - Fetch calendar/business day information
3. **Exchange Rate Data** - Fetch currency exchange rates

## Technology Stack
- Python FastAPI/MCP for the server implementation
- HTTPX for asynchronous HTTP requests
- Sentence Transformers for embeddings and semantic search
- Redis for optional caching (similar to current implementation)

## Migration Strategy

### Phase 1: Core Infrastructure
- Replace Kolada BASE_URL with Riksbanken OAuth implementation
- Update API client to handle Riksbanken authentication
- Create data models for Riksbanken entities

### Phase 2: Data Access Layer
- Implement Riksbanken API access services
- Create data processing utilities for Riksbanken's data format
- Build embeddings for Riksbanken's interest rate types and other entities

### Phase 3: Tool Implementation
- Develop tools that reflect Riksbanken's data structure
- Adapt existing tools where possible (search, metadata)
- Add new tools specific to financial data (e.g., exchange rates)

### Phase 4: Testing & Optimization
- Implement comprehensive tests for all tools
- Optimize data retrieval with caching
- Add rate limiting to respect Riksbanken API constraints

## Security Considerations
- Secure storage of API credentials
- Implement rate limiting to avoid overwhelming Riksbanken API
- Do not expose sensitive financial data

## Scalability Approach
- Implement caching for frequently accessed data
- Use asynchronous programming for API requests
- Structure for potential future expansion to additional financial APIs 