import requests

# Base URL for the deployed API
BASE_URL = "https://cgwb-backend.onrender.com"

def test_root():
    """Test the root endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print("Root Endpoint:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_groundwater():
    """Test the groundwater endpoint."""
    params = {
        "state": "Odisha",
        "district": "Baleshwar",
        "agency": "CGWB",
        "start_date": "2023-11-01",
        "end_date": "2024-10-31"
    }
    response = requests.get(f"{BASE_URL}/api/v1/groundwater", params=params)
    print("Groundwater Endpoint:")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Data Keys: {list(data.keys()) if isinstance(data, dict) else 'List of records'}")
        print(f"Sample Data: {data[:2] if isinstance(data, list) else data}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_rainfall():
    """Test the rainfall endpoint."""
    params = {
        "state": "Odisha",
        "district": "Baleshwar",
        "agency": "CGWB",
        "start_date": "2023-11-01",
        "end_date": "2024-10-31"
    }
    response = requests.get(f"{BASE_URL}/api/v1/rainfall", params=params)
    print("Rainfall Endpoint:")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Data Keys: {list(data.keys()) if isinstance(data, dict) else 'List of records'}")
        print(f"Sample Data: {data[:2] if isinstance(data, list) else data}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_analysis():
    """Test the groundwater analysis endpoint."""
    params = {
        "state": "Odisha",
        "district": "Baleshwar",
        "agency": "CGWB",
        "start_date": "2023-11-01",
        "end_date": "2024-10-31",
        "current_date": "2024-09-13",
        "period_months": 12
    }
    response = requests.get(f"{BASE_URL}/api/v1/groundwater-analysis", params=params)
    print("Groundwater Analysis Endpoint:")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Analysis Keys: {list(data.keys())}")
        print(f"Recharge Rate: {data.get('recharge_rate', 'N/A')}")
        print(f"Depletion Rate: {data.get('depletion_rate', 'N/A')}")
        print(f"Critical Level: {data.get('critical_level', 'N/A')}")
        print(f"Status: {data.get('status', 'N/A')}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_trends():
    """Test the groundwater trends endpoint."""
    params = {
        "state": "Odisha",
        "district": "Baleshwar",
        "agency": "CGWB",
        "start_date": "2023-11-01",
        "end_date": "2024-10-31"
    }
    response = requests.get(f"{BASE_URL}/api/v1/groundwater-trends", params=params)
    print("Groundwater Trends Endpoint:")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Trends Keys: {list(data.keys())}")
        print(f"Trend Slope: {data.get('trend_slope', 'N/A')}")
        print(f"Prediction: {data.get('prediction', 'N/A')}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Groundwater Resource Evaluation API Flow\n")
    test_root()
    test_groundwater()
    test_rainfall()
    test_analysis()
    test_trends()
    print("Testing complete!")