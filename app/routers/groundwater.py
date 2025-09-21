from fastapi import APIRouter, HTTPException
from app.services.wris_api_client import fetch_groundwater_data
from app.services.analysis_service import estimate_missing_groundwater_idw

router = APIRouter()

@router.get("/groundwater")
async def get_groundwater_data(
    state: str,
    district: str,
    agency: str,
    start_date: str,
    end_date: str,
    page: int = 0,
    size: int = 1000
):
    try:
        data = fetch_groundwater_data(state, district, agency, start_date, end_date, page, size)
        data_list = data.get('data', [])
        has_estimated = False

        # Consider only numeric dataValue as valid real observations
        numeric_values = [item for item in data_list if item.get('dataValue') is not None]

        if numeric_values:
            # Sort by dataTime descending and take the latest numeric record
            numeric_values.sort(key=lambda x: x.get('dataTime', ''), reverse=True)
            data['data'] = [numeric_values[0]]
            data['has_estimated_data'] = False
        else:
            # No numeric observations: try IDW estimation for the requested year
            year = int(start_date[:4])
            estimated_level = estimate_missing_groundwater_idw(state, district, year)
            if estimated_level is not None:
                data = {
                    "data": [{
                        "dataValue": estimated_level,
                        "dataTime": f"{year}-06-01T00:00:00",
                        "unit": "m",
                        "is_estimated": True,
                        "estimation_method": "IDW",
                        "stationCode": "N/A",
                        "stationName": "N/A",
                        "latitude": 0,
                        "longitude": 0,
                        "agencyName": agency,
                        "state": state,
                        "district": district,
                        "wellDepth": None
                    }],
                    "has_estimated_data": True
                }
                has_estimated = True
            else:
                data = {"data": [], "has_estimated_data": False}
            
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")