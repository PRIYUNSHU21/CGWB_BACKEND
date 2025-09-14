import pandas as pd
from typing import Dict, Any, List
import os

def fetch_groundwater_data(state: str, district: str, agency: str, start_date: str, end_date: str, page: int = 0, size: int = 1000) -> Dict[str, Any]:
    if not os.path.exists('groundwater_data.csv'):
        return {"statusCode": 404, "message": "Groundwater data file not found", "data": []}
    
    df = pd.read_csv('groundwater_data.csv')
    # Filter by state, district, agency
    filtered = df[(df['state'] == state) & (df['district'] == district)]
    if 'agency' in df.columns:
        filtered = filtered[filtered['agency'] == agency]
    # Since data is yearly, filter by year range if possible
    if 'year' in filtered.columns:
        start_year = int(start_date[:4])
        end_year = int(end_date[:4])
        filtered = filtered[(filtered['year'] >= start_year) & (filtered['year'] <= end_year)]
    
    # Paginate
    start_idx = page * size
    end_idx = start_idx + size
    paginated = filtered.iloc[start_idx:end_idx]
    
    data = []
    for _, row in paginated.iterrows():
        data.append({
            "dataTime": row.get('data_time', ''),
            "dataValue": None if pd.isna(row.get('data_value')) else row.get('data_value', 0),
            "unit": row.get('unit', 'm'),
            "stationCode": "N/A",
            "stationName": "N/A",
            "latitude": 0,
            "longitude": 0,
            "agencyName": row.get('agency', agency),
            "state": row.get('state', state),
            "district": row.get('district', district),
            "wellDepth": None if pd.isna(row.get('well_depth')) else row.get('well_depth', None)
        })
    
    return {
        "statusCode": 200,
        "message": "Data fetched successfully",
        "data": data
    }

def fetch_rainfall_data(state: str, district: str, agency: str, start_date: str, end_date: str, page: int = 0, size: int = 1000) -> Dict[str, Any]:
    if not os.path.exists('rainfall_data.csv'):
        return {"statusCode": 404, "message": "Rainfall data file not found", "data": []}
    
    df = pd.read_csv('rainfall_data.csv')
    # Filter by state, district, agency
    filtered = df[(df['state'] == state) & (df['district'] == district)]
    if 'agency' in df.columns:
        filtered = filtered[filtered['agency'] == agency]
    # Filter by year
    if 'year' in filtered.columns:
        start_year = int(start_date[:4])
        end_year = int(end_date[:4])
        filtered = filtered[(filtered['year'] >= start_year) & (filtered['year'] <= end_year)]
    
    # Paginate
    start_idx = page * size
    end_idx = start_idx + size
    paginated = filtered.iloc[start_idx:end_idx]
    
    data = []
    for _, row in paginated.iterrows():
        data.append({
            "dataTime": row.get('data_time', ''),
            "dataValue": None if pd.isna(row.get('data_value')) else row.get('data_value', 0),
            "unit": row.get('unit', 'mm'),
            "stationCode": "N/A",
            "stationName": "N/A",
            "latitude": 0,
            "longitude": 0,
            "agencyName": row.get('agency', agency),
            "state": row.get('state', state),
            "district": row.get('district', district)
        })
    
    return {
        "statusCode": 200,
        "message": "Data fetched successfully",
        "data": data
    }