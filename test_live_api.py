import requests

BASE_URL = "https://cgwb-backend.onrender.com/api/v1"

def test_root():
    response = requests.get("https://cgwb-backend.onrender.com/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")

def test_groundwater_analysis():
    payload = {
        "state": "West Bengal",
        "district": "Kolkata",  # Test with a district that might have data
        "agency": "CGWB",
        "start_date": "2020-01-01",
        "end_date": "2024-12-31"
    }
    response = requests.get(f"{BASE_URL}/groundwater-analysis", params=payload)
    print(f"Groundwater Analysis: {response.status_code}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)

def test_trends():
    params = {
        "state": "West Bengal",
        "district": "Kolkata",
        "agency": "CGWB",
        "historical_months": 24,
        "forecast_months": 12
    }
    response = requests.get(f"{BASE_URL}/groundwater-trends", params=params)
    print(f"Trends: {response.status_code}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)

def test_groundwater_data():
    params = {
        "state": "West Bengal",
        "district": "Kolkata",
        "agency": "CGWB",
        "start_date": "2020-01-01",
        "end_date": "2024-12-31"
    }
    response = requests.get(f"{BASE_URL}/groundwater", params=params)
    print(f"Groundwater Data: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Data points: {len(data.get('data', []))}")
    else:
        print(response.text)

def test_rainfall_data():
    params = {
        "state": "West Bengal",
        "district": "Kolkata",
        "agency": "CWC",  # Rainfall data uses CWC agency
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    response = requests.get(f"{BASE_URL}/rainfall", params=params)
    print(f"Rainfall Data: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Data points: {len(data.get('data', []))}")
    else:
        print(response.text)

if __name__ == "__main__":
    print("Testing Groundwater Resource Evaluation API")
    test_root()
    test_groundwater_data()
    test_rainfall_data()
    test_groundwater_analysis()
    test_trends()