from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import groundwater, rainfall, analysis

app = FastAPI(title="Groundwater Resource Evaluation API", version="1.0.0")

# CORS middleware: configure allowed origins for development and production
# In production, replace "*" with an explicit list of allowed frontend origins.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://your-frontend-domain.com",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(groundwater, prefix="/api/v1", tags=["Groundwater"])
app.include_router(rainfall, prefix="/api/v1", tags=["Rainfall"])
app.include_router(analysis, prefix="/api/v1", tags=["Analysis"])


@app.get("/")
async def root():
    return {"message": "Welcome to Groundwater Resource Evaluation API"}