# Groundwater Resource Evaluation Backend

This is a Python backend API for groundwater resource evaluation using local CSV data files.

## Features

- Load groundwater level data from `groundwater_data.csv`
- Load rainfall data from `rainfall_data.csv`
- Calculate groundwater recharge rate using soil-based infiltration coefficients
- Assess depletion rate from historical yearly data
- Detect critical groundwater levels
- Compare regeneration to depletion for sustainability analysis
- Predict trends using linear regression on yearly data
- RESTful API endpoints for mobile app integration

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Ensure data files are present:
   - `groundwater_data.csv` (columns: state, district, year, data_value, unit, data_time, agency, well_depth)
   - `rainfall_data.csv` (columns: state, district, year, data_value, unit, data_time, agency)

3. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

4. Access the API documentation at http://127.0.0.1:8000/docs

## API Endpoints

- GET /api/v1/groundwater?state=...&district=...&agency=...&start_date=...&end_date=...
- GET /api/v1/rainfall?state=...&district=...&agency=...&start_date=...&end_date=...
- GET /api/v1/groundwater-analysis?state=...&district=...&agency=...&start_date=...&end_date=...&current_date=...&period_months=...
- GET /api/v1/groundwater-trends?state=...&district=...&agency=...&historical_months=24&forecast_months=12

## Data Source

Data is loaded from local CSV files. Originally sourced from India WRIS API, but now stored locally for offline analysis.

## Soil Coefficients

Refer to soil_coefficients.md for infiltration factors used in recharge calculations.