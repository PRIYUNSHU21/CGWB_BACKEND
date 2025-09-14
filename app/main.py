from fastapi import FastAPI
from app.routers import groundwater, rainfall, analysis

app = FastAPI(title="Groundwater Resource Evaluation API", version="1.0.0")

app.include_router(groundwater, prefix="/api/v1", tags=["Groundwater"])
app.include_router(rainfall, prefix="/api/v1", tags=["Rainfall"])
app.include_router(analysis, prefix="/api/v1", tags=["Analysis"])

@app.get("/")
async def root():
    return {"message": "Welcome to Groundwater Resource Evaluation API"}