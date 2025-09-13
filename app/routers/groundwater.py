from fastapi import APIRouter, HTTPException
import requests
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
        return data
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")