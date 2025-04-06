# STORY-006: Define core data models for interest rates

## Description
As a developer, I need to define the core data models to represent interest rate data from Riksbanken, replacing the existing Kolada KPI models, to ensure proper typing and data structure throughout the application.

## Acceptance Criteria
- [ ] Create data models for interest rate types
- [ ] Create data models for interest rate data points
- [ ] Update the application's type system to use these models
- [ ] Ensure models include all necessary fields from Riksbanken's API responses
- [ ] Create serialization/deserialization methods if needed
- [ ] Add appropriate type hints throughout the codebase
- [ ] Document the data model structure

## Implementation Notes
- Review existing KPI models in `src/models/types.py`
- Replace `KoladaKpi` with `RiksbankInterestRate` model
- Consider using Pydantic models for automatic validation
- Interest rate models should include:
  - Interest rate ID
  - Name/title 
  - Description
  - Category (if applicable)
  - Date range availability
- Interest rate data points should include:
  - Value
  - Date
  - Status (if applicable)

## Dependencies
- STORY-005: Implement TORA API integration (can be developed in parallel)

## Estimated Effort
Small: 1-2 days

## Status
Planned

## Test Scenarios
1. Test model instantiation with valid data
2. Test validation of required fields
3. Test serialization/deserialization if implemented
4. Test model compatibility with API response formats 