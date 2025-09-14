from fastapi import APIRouter, HTTPException
from app.services.wris_api_client import fetch_rainfall_data

router = APIRouter()

@router.get("/rainfall")
async def get_rainfall_data(
    state: str,
    district: str,
    agency: str,
    start_date: str,
    end_date: str,
    page: int = 0,
    size: int = 1000
):
    try:
        data = fetch_rainfall_data(state, district, agency, start_date, end_date, page, size)
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")