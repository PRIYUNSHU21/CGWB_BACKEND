from fastapi import APIRouter, HTTPException
from app.services.wris_api_client import fetch_groundwater_data

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
        if data_list:
            # Sort by dataTime descending and take the latest
            data_list.sort(key=lambda x: x.get('dataTime', ''), reverse=True)
            data['data'] = [data_list[0]]
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")