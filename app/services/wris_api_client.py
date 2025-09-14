import requests
from typing import Dict, Any, List

BASE_URL = "https://indiawris.gov.in"

def fetch_groundwater_data(state: str, district: str, agency: str, start_date: str, end_date: str, page: int = 0, size: int = 1000) -> Dict[str, Any]:
    url = f"{BASE_URL}/Dataset/Ground Water Level"
    params = {
        "stateName": state,
        "districtName": district,
        "agencyName": agency,
        "startdate": start_date,
        "enddate": end_date,
        "download": False,
        "page": page,
        "size": size
    }
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "accept": "application/json"}
        response = requests.post(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        status_code = data.get("statusCode")
        if status_code is not None and status_code != 200:
            raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")
        return data
    except requests.RequestException as e:
        raise ValueError(f"Request failed: {str(e)}")
    except ValueError as e:
        raise e

def fetch_rainfall_data(state: str, district: str, agency: str, start_date: str, end_date: str, page: int = 0, size: int = 1000) -> Dict[str, Any]:
    url = f"{BASE_URL}/Dataset/RainFall"
    params = {
        "stateName": state,
        "districtName": district,
        "agencyName": agency,
        "startdate": start_date,
        "enddate": end_date,
        "download": False,
        "page": page,
        "size": size
    }
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "accept": "application/json"}
        response = requests.post(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        status_code = data.get("statusCode")
        if status_code is not None and status_code != 200:
            raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")
        return data
    except requests.RequestException as e:
        raise ValueError(f"Request failed: {str(e)}")
    except ValueError as e:
        raise e