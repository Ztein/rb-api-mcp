# Riksbanken MCP Server - Minimum Viable Product

## MVP Definition
The Minimum Viable Product (MVP) for the Riksbanken MCP Server will provide LLMs with the ability to access and analyze Sweden's central bank (Riksbanken) financial data through a RESTful API. The MVP will focus on core functionality for authentication, data retrieval, and basic analysis tools.

## Core Features for MVP

### 1. Authentication & API Access
- OAuth2 authentication with Riksbanken APIs
- Token management and refresh mechanism
- Basic error handling and logging

### 2. Data Retrieval
- Interest rate data from TORA API
- Calendar/business day information from SWEA API
- Basic data caching for improved performance

### 3. MCP Tools
- Tool for listing available interest rate types
- Tool for retrieving specific interest rate data
- Tool for checking business days
- Basic search functionality for interest rate types

### 4. Data Analysis
- Basic time series data formatting
- Simple statistical analysis (min, max, average) for interest rates

## Out of Scope for MVP
The following features will be considered for future releases but are not part of the MVP:
- Advanced analysis tools for correlation between different rates
- Exchange rate data retrieval and analysis
- Visualization tools or dashboard integration
- Advanced embedding and semantic search capabilities
- Historical trend analysis

## Technical Components for MVP

### API Integration
- Base service for Riksbanken API interaction
- SWEA API integration for calendar data
- TORA API integration for interest rate data

### Data Models
- Interest rate data models
- Calendar day data models
- API response models

### MCP Server Configuration
- FastMCP server configuration
- Tool registration
- Basic entry point prompt

## Success Criteria for MVP
The MVP will be considered successful when:

1. An LLM can successfully authenticate with Riksbanken APIs through the MCP server
2. Interest rate data can be retrieved and presented in a structured format
3. Basic queries about interest rates and business days can be answered
4. The system maintains high availability and responds within acceptable time limits
5. Error handling correctly manages and reports API issues 