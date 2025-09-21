from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.services.wris_api_client import fetch_groundwater_data, fetch_rainfall_data
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from scipy.spatial.distance import cdist
from district_coords import DISTRICT_COORDS

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

# Soil-based infiltration coefficients (from soil_coefficients.md)
SOIL_COEFFICIENT_MAP = {
    "Uttar Pradesh": 0.35,  # Alluvial
    "Bihar": 0.35,
    "West Bengal": 0.35,
    "Punjab": 0.35,
    "Haryana": 0.35,
    "Maharashtra": 0.15,  # Black
    "Gujarat": 0.15,  # Black/Desert/Saline/Alkaline - average 0.2
    "Madhya Pradesh": 0.15,
    "Karnataka": 0.15,  # Black/Red/Laterite - average 0.27
    "Tamil Nadu": 0.4,  # Red
    "Andhra Pradesh": 0.4,
    "Odisha": 0.32,  # Red/Laterite - average
    "Kerala": 0.25,  # Laterite
    "Rajasthan": 0.29,  # Desert/Alkaline - average
    "Uttarakhand": 0.25,  # Mountain
    "Himachal Pradesh": 0.25,
    "Arunachal Pradesh": 0.32,  # Mountain/Forest - average
    "Assam": 0.26,  # Peat/Forest - average
    "Meghalaya": 0.4,  # Forest
    "default": 0.3  # National average
}

# District-specific infiltration factors for West Bengal (based on soil types)
DISTRICT_INFILTRATION = {
    # Gangetic Plains - Alluvial soils (high infiltration)
    "Kolkata": 0.40,
    "Nadia": 0.38,
    "Murshidabad": 0.38,
    "Hooghly": 0.37,
    "Howrah": 0.36,
    "North 24 Parganas": 0.38,
    "South 24 Parganas": 0.37,
    
    # Hilly/Mountainous - Forest/Mountain soils (low infiltration)
    "Darjeeling": 0.25,
    "Jalpaiguri": 0.28,
    "Alipurduar": 0.27,
    
    # Red Laterite/Red soils (medium infiltration)
    "Birbhum": 0.32,
    "Bankura": 0.33,
    "Jhargram": 0.31,
    "Purulia": 0.30,
    
    # Coastal/Saline (variable)
    "Medinipur": 0.34,
    "Purba Medinipur": 0.34,
    "Paschim Medinipur": 0.33,
    
    # Default for West Bengal districts not listed
    "default_wb": 0.35
}

CRITICAL_THRESHOLD = 5.0  # m below ground
LOW_THRESHOLD = 10.0

def get_infiltration_factor(state: str, district: str = None) -> float:
    if state == "West Bengal" and district:
        return DISTRICT_INFILTRATION.get(district, DISTRICT_INFILTRATION.get("default_wb", 0.35))
    return SOIL_COEFFICIENT_MAP.get(state, SOIL_COEFFICIENT_MAP["default"])

def estimate_missing_groundwater_idw(state: str, district: str, year: int, power: int = 2, max_distance: float = 10.0):
    """
    Estimate groundwater level for a missing district using Inverse Distance Weighting (IDW).
    max_distance in degrees (approx 5° ~ 500km at equator).
    """
    if district not in DISTRICT_COORDS:
        return None  # No coordinates, can't estimate
    
    target_coord = np.array(DISTRICT_COORDS[district])
    known_values = []
    distances = []

    # For each other district, attempt to find same-year data only (expand radius instead of using past years)
    for d, coord in DISTRICT_COORDS.items():
        if d == district:
            continue
        gw_data = fetch_groundwater_data(state, d, "CGWB", f"{year}-01-01", f"{year}-12-31")
        data_list = gw_data.get('data', [])
        if not data_list:
            continue

        vals = [item.get('dataValue') for item in data_list if item.get('dataValue') is not None]
        if not vals:
            continue

        level = float(sum(vals) / len(vals))
        # Use haversine distance in km
        dist = haversine_distance(target_coord[0], target_coord[1], coord[0], coord[1])
        if dist > max_distance:
            continue
        if dist == 0:
            return float(level)
        known_values.append(level)
        distances.append(dist)
    
    if not known_values:
        return None  # No known data within range
    
    distances = np.array(distances)

    # IDW calculation (handle any tiny distances safely)
    # Add a small epsilon to distances to avoid division by zero (but zero handled above)
    eps = 1e-8
    weights = 1.0 / ((distances + eps) ** power)
    weights /= np.sum(weights)
    estimate = float(np.sum(np.array(known_values) * weights))

    return estimate

def calculate_recharge_rate(state: str, district: str, agency: str, start_date: str, end_date: str) -> float:
    rainfall_data = fetch_rainfall_data(state, district, agency, start_date, end_date)
    data_list = rainfall_data.get('data', [])
    if not isinstance(data_list, list):
        data_list = []
    total_rainfall = sum(item.get('dataValue', 0) for item in data_list)
    factor = get_infiltration_factor(state, district)
    return total_rainfall * factor

def calculate_depletion_rate(state: str, district: str, agency: str, current_date: str, period_months: int = 12) -> float:
    current_year = int(current_date[:4])
    past_year = current_year - (period_months // 12)
    
    current_data = fetch_groundwater_data(state, district, agency, f"{current_year}-01-01", f"{current_year}-12-31")
    past_data = fetch_groundwater_data(state, district, agency, f"{past_year}-01-01", f"{past_year}-12-31")
    
    current_list = current_data.get('data', [])
    if not isinstance(current_list, list):
        current_list = []
    past_list = past_data.get('data', [])
    if not isinstance(past_list, list):
        past_list = []
    
    if not current_list or not past_list:
        return 0.0
    
    # Average levels for the year
    current_level = sum(item.get('dataValue', 0) for item in current_list) / len(current_list) if current_list else 0
    past_level = sum(item.get('dataValue', 0) for item in past_list) / len(past_list) if past_list else 0
    time_years = period_months / 12
    depletion = (past_level - current_level) / time_years if time_years > 0 else 0
    return max(depletion, 0)

def check_critical_levels(groundwater_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    data_list = groundwater_data.get('data', [])
    if not isinstance(data_list, list):
        data_list = []
    results = []
    for item in data_list:
        level = item.get('dataValue', float('inf'))
        if level <= CRITICAL_THRESHOLD:
            status = "Critical"
        elif level <= LOW_THRESHOLD:
            status = "Low"
        else:
            status = "Normal"
        results.append({**item, "status": status})
    return results

def compare_to_regeneration(recharge_rate: float, current_level: float, state: str, district: str, agency: str, current_date: str) -> str:
    depletion_rate = calculate_depletion_rate(state, district, agency, current_date)
    net_change = recharge_rate - depletion_rate
    if net_change > 0:
        return "Sustainable" if current_level > CRITICAL_THRESHOLD else "Improving"
    elif net_change < 0 and current_level <= CRITICAL_THRESHOLD:
        return "Unsustainable"
    else:
        return "Stable"

def analyze_groundwater(state: str, district: str, agency: str, start_date: str, end_date: str, current_date: str = None, period_months: int = 12) -> Dict[str, Any]:
    if not current_date:
        current_date = end_date
    gw_data = fetch_groundwater_data(state, district, agency, start_date, end_date)
    
    # Filter to latest data point
    data_list = gw_data.get('data', [])
    if data_list:
        data_list.sort(key=lambda x: x.get('dataTime', ''), reverse=True)
        gw_data['data'] = [data_list[0]]
        data_list = gw_data["data"]
    
    # If no data, estimate using IDW
    has_estimated = False
    if not data_list:
        year = int(start_date[:4])
        estimated_level = estimate_missing_groundwater_idw(state, district, year)
        if estimated_level > 0:
            gw_data = {
                "data": [{
                    "dataValue": estimated_level,
                    "dataTime": f"{year}-06-01T00:00:00",
                    "unit": "m",
                    "is_estimated": True,
                    "estimation_method": "IDW"
                }]
            }
            data_list = gw_data["data"]
            has_estimated = True
    else:
        # Check if any existing data is estimated (though currently not)
        for item in data_list:
            if item.get("is_estimated"):
                has_estimated = True
                break
    
    recharge = calculate_recharge_rate(state, district, agency, start_date, end_date)
    analyzed_data = check_critical_levels(gw_data)
    for item in analyzed_data:
        item["regeneration_status"] = compare_to_regeneration(recharge, item.get('dataValue', 0), state, district, agency, current_date)
    depletion = calculate_depletion_rate(state, district, agency, current_date, period_months)
    return {
        "groundwater_data": analyzed_data,
        "recharge_rate": round(recharge if not np.isnan(recharge) else 0.0, 4),
        "depletion_rate": round(depletion if not np.isnan(depletion) else 0.0, 4),
        "has_estimated_data": has_estimated,
        "unit": "m/year"
    }

def predict_trends(state: str, district: str, agency: str, historical_months: int = 24, forecast_months: int = 12) -> Dict[str, Any]:
    """Predict groundwater level trends using linear regression on yearly data."""
    historical_years = historical_months // 12
    current_year = datetime.now().year
    start_year = current_year - historical_years
    
    # Fetch yearly data
    years = []
    levels = []
    has_estimated_levels = False
    for year in range(start_year, current_year):
        data = fetch_groundwater_data(state, district, agency, f"{year}-01-01", f"{year}-12-31")
        data_list = data.get('data', [])
        if not isinstance(data_list, list):
            data_list = []
        if data_list:
            level = sum(item.get('dataValue', 0) for item in data_list) / len(data_list)
        else:
            # Estimate if missing
            level = estimate_missing_groundwater_idw(state, district, year)
            if level == 0.0:
                level = None  # Mark as missing for interpolation
            else:
                has_estimated_levels = True
        years.append(year)
        levels.append(level)
    
    # Interpolate missing values
    valid_years = [y for y, l in zip(years, levels) if l is not None]
    valid_levels = [l for l in levels if l is not None]
    if len(valid_years) >= 2:
        interpolated_levels = np.interp(years, valid_years, valid_levels)
        levels = interpolated_levels.tolist()
    else:
        # If not enough valid points, use only valid ones
        years = valid_years
        levels = valid_levels
    
    if len(years) < 2:
        return {"error": "Insufficient historical data for trend analysis"}
    
    # Fit linear regression
    X = np.array(years).reshape(-1, 1)
    y = np.array(levels)
    model = LinearRegression()
    model.fit(X, y)
    
    slope = model.coef_[0]  # Change per year
    r_squared = model.score(X, y)
    trend = "Declining" if slope < 0 else "Recovering" if slope > 0 else "Stable"
    
    # Forecast future years
    forecast_years = [current_year + i for i in range(1, (forecast_months // 12) + 1)]
    future_X = np.array(forecast_years).reshape(-1, 1)
    predictions = model.predict(future_X)
    
    return {
        "trend_slope": round(slope, 4),
        "trend_status": trend,
        "r_squared": round(r_squared, 4),
        "historical_levels": [round(l, 4) for l in levels],
        "predicted_levels": [round(p, 4) for p in predictions.tolist()],
        "has_estimated_levels": has_estimated_levels,
        "forecast_period_years": len(forecast_years),
        "unit": "m/year"
    }