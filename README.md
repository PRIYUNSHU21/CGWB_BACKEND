# Groundwater Resource Evaluation Backend

This is a Python backend API for real-time groundwater resource evaluation using data from India WRIS (Water Resources Information System) API.

## Features

- Fetch groundwater level data from DWLR stations
- Fetch rainfall data
- Calculate groundwater recharge rate using soil-based infiltration coefficients
- Assess depletion rate from historical data
- Detect critical groundwater levels
- Compare regeneration to depletion for sustainability analysis
- RESTful API endpoints for mobile app integration

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

3. Access the API documentation at http://127.0.0.1:8000/docs

## API Endpoints

- GET /api/v1/groundwater?state=...&district=...&agency=...&start_date=...&end_date=...
- GET /api/v1/rainfall?state=...&district=...&agency=...&start_date=...&end_date=...
- GET /api/v1/groundwater-analysis?state=...&district=...&agency=...&start_date=...&end_date=...&current_date=...&period_months=...
- GET /api/v1/groundwater-trends?state=...&district=...&agency=...&historical_months=24&forecast_months=12

## Data Source

Data is fetched from India WRIS API: https://indiawris.gov.in

## Soil Coefficients

Refer to soil_coefficients.md for infiltration factors used in recharge calculations.