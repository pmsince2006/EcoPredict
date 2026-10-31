"""Air Quality and Forecasting API route handlers."""
try:
    from fastapi import APIRouter, Query
except ImportError:
    class APIRouter:
        def __init__(self, *args, **kwargs):
            pass
        def get(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator
    def Query(default=None, **kwargs):
        return default

from app.services.aqi_service import AQIService

router = APIRouter(prefix="/aqi", tags=["Air Quality"])


@router.get("/summary")
def get_aqi_summary(location: str = Query(default="Delhi NCR")):
    """Returns the current summary reading for a selected monitoring area."""
    return AQIService.get_demo_summary(location=location)


@router.get("/stations")
def get_monitoring_stations():
    """Returns geospatial monitoring stations with current sensor levels."""
    return {
        "stations": AQIService.get_demo_stations(),
        "is_demo_data": True,
    }
