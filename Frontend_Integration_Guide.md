# Frontend Integration Guide

## Overview
This guide provides comprehensive instructions for integrating with the Groundwater Evaluation API. The API offers endpoints for accessing groundwater data, rainfall information, and advanced analysis features including spatial interpolation and trend analysis.

## Hosted Link
**Base URL**: `https://cgwb-backend.onrender.com`
*Note: Replace with your actual Render deployment URL if different*

## API Endpoints

### 1. Groundwater Data Endpoint
**Endpoint**: `GET /groundwater`

**Purpose**: Retrieves the latest groundwater level data for a specified district, with automatic IDW estimation if local data is unavailable.

**Parameters**:
- `district` (string, required): Name of the district (e.g., "Kolkata", "Darjeeling")
- `year` (integer, optional): Specific year for data (defaults to latest available)
- `month` (string, optional): Specific month for data (defaults to latest available)

**Request Example**:
```
GET https://cgwb-backend.onrender.com/groundwater?district=Kolkata
```

**Response Format**:
```json
{
  "district": "Kolkata",
  "year": 2023,
  "month": "December",
  "water_level": 4.2,
  "estimated": false,
  "data_points_used": 12,
  "nearest_districts": ["Howrah", "North 24 Parganas"]
}
```

**Response Fields**:
- `district`: Requested district name
- `year`: Year of the data
- `month`: Month of the data
- `water_level`: Groundwater level in meters
- `estimated`: Boolean indicating if value was estimated using IDW
- `data_points_used`: Number of data points used for estimation (if estimated)
- `nearest_districts`: Array of districts used for IDW calculation (if estimated)

### 2. Rainfall Data Endpoint
**Endpoint**: `GET /rainfall`

**Purpose**: Retrieves rainfall data for a specified district.

**Parameters**:
- `district` (string, required): Name of the district
- `year` (integer, optional): Specific year (defaults to 2024)
- `month` (string, optional): Specific month

**Request Example**:
```
GET https://cgwb-backend.onrender.com/rainfall?district=Kolkata&year=2024&month=January
```

**Response Format**:
```json
{
  "district": "Kolkata",
  "year": 2024,
  "month": "January",
  "rainfall_mm": 12.5,
  "data_available": true
}
```

**Response Fields**:
- `district`: Requested district name
- `year`: Year of the data
- `month`: Month of the data
- `rainfall_mm`: Rainfall in millimeters
- `data_available`: Boolean indicating if data exists for the request

### 3. Groundwater Analysis Endpoint
**Endpoint**: `GET /groundwater-analysis`

**Purpose**: Provides comprehensive groundwater analysis including current levels, recharge/depletion rates, and critical level assessment.

**Parameters**:
- `district` (string, required): Name of the district
- `current_date` (string, optional): Date for analysis in YYYY-MM-DD format (defaults to today)

**Request Example**:
```
GET https://cgwb-backend.onrender.com/groundwater-analysis?district=Kolkata&current_date=2025-09-15
```

**Response Format**:
```json
{
  "district": "Kolkata",
  "current_level": 4.2,
  "estimated": false,
  "recharge_rate": 0.15,
  "depletion_rate": -0.08,
  "critical_level": 5.0,
  "is_critical": false,
  "infiltration_factor": 0.85,
  "analysis_date": "2025-09-15",
  "data_quality": "high"
}
```

**Response Fields**:
- `district`: Analyzed district name
- `current_level`: Current groundwater level in meters
- `estimated`: Boolean indicating if current level was estimated
- `recharge_rate`: Annual recharge rate in meters/year
- `depletion_rate`: Annual depletion rate in meters/year
- `critical_level`: Critical groundwater level threshold in meters
- `is_critical`: Boolean indicating if current level is below critical threshold
- `infiltration_factor`: District-specific soil infiltration factor (0-1)
- `analysis_date`: Date of analysis
- `data_quality`: Quality assessment ("high", "medium", "low")

### 4. Groundwater Trends Endpoint
**Endpoint**: `GET /groundwater-trends`

**Purpose**: Provides historical trends and future projections of groundwater levels using polynomial regression.

**Parameters**:
- `district` (string, required): Name of the district
- `projection_years` (integer, optional): Number of years to project forward (default: 5)
- `include_historical` (boolean, optional): Include historical data points (default: true)

**Request Example**:
```
GET https://cgwb-backend.onrender.com/groundwater-trends?district=Kolkata&projection_years=3&include_historical=true
```

**Response Format**:
```json
{
  "district": "Kolkata",
  "historical_data": [
    {"year": 2020, "level": 5.1, "estimated": false},
    {"year": 2021, "level": 4.9, "estimated": false},
    {"year": 2022, "level": 4.5, "estimated": true}
  ],
  "projections": [
    {"year": 2024, "level": 4.2, "estimated": false},
    {"year": 2025, "level": 4.0, "estimated": true},
    {"year": 2026, "level": 3.8, "estimated": true}
  ],
  "trend_analysis": {
    "r_squared": 0.87,
    "trend_direction": "decreasing",
    "average_rate": -0.12,
    "has_estimated_levels": true
  },
  "model_info": {
    "polynomial_degree": 2,
    "regularization_alpha": 0.1,
    "training_data_points": 24
  }
}
```

**Response Fields**:
- `district`: Analyzed district name
- `historical_data`: Array of historical groundwater levels
  - `year`: Year of measurement
  - `level`: Groundwater level in meters
  - `estimated`: Boolean indicating if level was estimated
- `projections`: Array of projected future levels
  - `year`: Projected year
  - `level`: Projected level in meters
  - `estimated`: Boolean indicating if projection uses estimated data
- `trend_analysis`: Trend analysis results
  - `r_squared`: Goodness-of-fit metric (0-1)
  - `trend_direction`: "increasing", "decreasing", or "stable"
  - `average_rate`: Average annual change in meters/year
  - `has_estimated_levels`: Boolean indicating if any data points were estimated
- `model_info`: Details about the regression model
  - `polynomial_degree`: Degree of polynomial used
  - `regularization_alpha`: Ridge regularization parameter
  - `training_data_points`: Number of data points used for training

## Request Format Guidelines

### HTTP Method
All endpoints use **GET** requests with query parameters.

### Parameter Encoding
- Use URL encoding for special characters in district names
- Dates should be in ISO format (YYYY-MM-DD)
- Boolean parameters accept "true"/"false" or "1"/"0"

### Error Handling
The API returns standard HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (district not found)
- `500`: Internal Server Error

**Error Response Format**:
```json
{
  "error": "District not found",
  "message": "Please check the district name and try again",
  "status_code": 404
}
```

## Integration Best Practices

### 1. Estimation Flags
Always check the `estimated` field in responses. If `true`, inform users that the data is spatially interpolated.

### 2. Data Quality Assessment
Use the `data_quality` field in analysis responses to gauge reliability.

### 3. Rate Limiting
Implement client-side caching to avoid excessive API calls. Consider rate limits if deploying at scale.

### 4. Error Handling
Implement robust error handling for network failures and invalid responses.

### 5. Data Validation
Validate district names against the known list of 23 West Bengal districts.

## Supported Districts
The API supports the following districts:
- Kolkata
- Howrah
- North 24 Parganas
- South 24 Parganas
- Darjeeling
- And 18 others...

*Note: Full list available in the district_coords.py file*

## Authentication
Currently, no authentication is required. Consider adding API keys for production deployments.

## Versioning
API version is included in the base path: `/v1/` (not yet implemented but planned for future updates).

This guide should provide everything needed for successful frontend integration with the Groundwater Evaluation API.