from fastapi import APIRouter, HTTPException
from app.services.analysis_service import analyze_groundwater, predict_trends

router = APIRouter()

@router.get("/groundwater-analysis")
async def get_groundwater_analysis(
    state: str,
    district: str,
    agency: str,
    start_date: str,
    end_date: str,
    current_date: str = None,
    period_months: int = 12
):
    try:
        result = analyze_groundwater(state, district, agency, start_date, end_date, current_date, period_months)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@router.get("/groundwater-trends")
async def get_groundwater_trends(
    state: str,
    district: str,
    agency: str,
    historical_months: int = 24,
    forecast_months: int = 12
):
    try:
        result = predict_trends(state, district, agency, historical_months, forecast_months)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend prediction error: {str(e)}")