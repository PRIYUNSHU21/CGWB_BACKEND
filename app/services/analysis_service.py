from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.services.wris_api_client import fetch_groundwater_data, fetch_rainfall_data
import numpy as np
from sklearn.linear_model import LinearRegression

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

CRITICAL_THRESHOLD = 5.0  # m below ground
LOW_THRESHOLD = 10.0

def get_infiltration_factor(state: str) -> float:
    return SOIL_COEFFICIENT_MAP.get(state, SOIL_COEFFICIENT_MAP["default"])

def calculate_recharge_rate(state: str, district: str, agency: str, start_date: str, end_date: str) -> float:
    rainfall_data = fetch_rainfall_data(state, district, agency, start_date, end_date)
    data_list = rainfall_data.get('data', [])
    if not isinstance(data_list, list):
        data_list = []
    total_rainfall = sum(item.get('dataValue', 0) for item in data_list)
    factor = get_infiltration_factor(state)
    return total_rainfall * factor

def calculate_depletion_rate(state: str, district: str, agency: str, current_date: str, period_months: int = 12) -> float:
    current_data = fetch_groundwater_data(state, district, agency, current_date, current_date)
    past_date = (datetime.fromisoformat(current_date) - timedelta(days=period_months * 30)).isoformat()[:10]
    past_data = fetch_groundwater_data(state, district, agency, past_date, past_date)
    
    current_list = current_data.get('data', [])
    if not isinstance(current_list, list):
        current_list = []
    past_list = past_data.get('data', [])
    if not isinstance(past_list, list):
        past_list = []
    
    if not current_list or not past_list:
        return 0.0
    
    current_level = current_list[0].get('dataValue', 0)
    past_level = past_list[0].get('dataValue', 0)
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
    recharge = calculate_recharge_rate(state, district, agency, start_date, end_date)
    analyzed_data = check_critical_levels(gw_data)
    for item in analyzed_data:
        item["regeneration_status"] = compare_to_regeneration(recharge, item.get('dataValue', 0), state, district, agency, current_date)
    return {
        "groundwater_data": analyzed_data,
        "recharge_rate": recharge,
        "depletion_rate": calculate_depletion_rate(state, district, agency, current_date, period_months),
        "unit": "m/year"
    }

def predict_trends(state: str, district: str, agency: str, historical_months: int = 24, forecast_months: int = 12) -> Dict[str, Any]:
    """Predict groundwater level trends using linear regression."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=historical_months * 30)
    
    # Fetch historical data (simplified: assume monthly data points)
    dates = []
    levels = []
    current = start_date
    while current <= end_date:
        data = fetch_groundwater_data(state, district, agency, current.isoformat(), current.isoformat())
        data_list = data.get('data', [])
        if not isinstance(data_list, list):
            data_list = []
        if data_list:
            level = data_list[0].get('dataValue', 0)
            dates.append((current - start_date).days)  # Days since start
            levels.append(level)
        current += timedelta(days=30)  # Monthly
    
    if len(dates) < 2:
        return {"error": "Insufficient historical data for trend analysis"}
    
    # Fit linear regression
    X = np.array(dates).reshape(-1, 1)
    y = np.array(levels)
    model = LinearRegression()
    model.fit(X, y)
    
    slope = model.coef_[0]  # Change per day
    trend = "Declining" if slope < 0 else "Recovering" if slope > 0 else "Stable"
    
    # Forecast future levels
    future_dates = np.array([max(dates) + i * 30 for i in range(1, forecast_months + 1)]).reshape(-1, 1)
    predictions = model.predict(future_dates)
    
    return {
        "trend_slope": slope * 30,  # Per month
        "trend_status": trend,
        "historical_levels": levels,
        "predicted_levels": predictions.tolist(),
        "forecast_period_months": forecast_months,
        "unit": "m/month"
    }