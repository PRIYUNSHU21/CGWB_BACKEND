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
        if data_list:
            # Sort by dataTime descending and take the latest
            data_list.sort(key=lambda x: x.get('dataTime', ''), reverse=True)
            data['data'] = [data_list[0]]
        else:
            # No real data, provide IDW estimate
            year = int(start_date[:4])
            estimated_level = estimate_missing_groundwater_idw(state, district, year)
            if estimated_level > 0:
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
                data['has_estimated_data'] = False
        
        if not has_estimated and data_list:
            data['has_estimated_data'] = False
        elif has_estimated:
            data['has_estimated_data'] = True
            
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")