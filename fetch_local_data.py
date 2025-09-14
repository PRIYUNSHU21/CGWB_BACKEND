import requests
import json
import os

BASE_URL = "https://indiawris.gov.in"
HEADERS = {"accept": "application/json"}

# Districts for Odisha
districts = ["Baleshwar", "Cuttack"]
years = ["2023", "2024"]

for district in districts:
    for year in years:
        print(f"Fetching data for {district}, {year}...")
        
        # Groundwater
        params = {
            "stateName": "Odisha",
            "districtName": district,
            "agencyName": "CGWB",
            "startdate": f"{year}-01-01",
            "enddate": f"{year}-12-31",
            "download": False,
            "page": 0,
            "size": 50
        }
        try:
            response = requests.post(f"{BASE_URL}/Dataset/Ground Water Level", params=params, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                with open(f"odisha_{district}_groundwater_{year}.json", "w") as f:
                    json.dump(response.json(), f)
                print(f"Saved groundwater data for {district}, {year}")
            else:
                print(f"Failed to fetch groundwater for {district}, {year}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching groundwater for {district}, {year}: {e}")

        # Rainfall
        params["agencyName"] = "CWC"
        try:
            response = requests.post(f"{BASE_URL}/Dataset/RainFall", params=params, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                with open(f"odisha_{district}_rainfall_{year}.json", "w") as f:
                    json.dump(response.json(), f)
                print(f"Saved rainfall data for {district}, {year}")
            else:
                print(f"Failed to fetch rainfall for {district}, {year}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching rainfall for {district}, {year}: {e}")

print("Data fetching complete!")