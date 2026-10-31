"""Pydantic data models for Air Quality metrics, forecasts, and monitoring stations."""

from typing import List, Optional
try:
    from pydantic import BaseModel, Field
except ImportError:
    # Graceful fallback for basic linting when pydantic is not yet installed in local env
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(*args, **kwargs):
        return kwargs.get("default", None)


class PollutantMetrics(BaseModel):
    """Concentrations of individual air pollutants."""
    pm25: float = Field(default=0.0, description="PM2.5 concentration in µg/m³")
    pm10: float = Field(default=0.0, description="PM10 concentration in µg/m³")
    no2: float = Field(default=0.0, description="NO2 concentration in µg/m³")
    so2: float = Field(default=0.0, description="SO2 concentration in µg/m³")
    co: float = Field(default=0.0, description="CO concentration in mg/m³")
    o3: float = Field(default=0.0, description="O3 concentration in µg/m³")


class AQISummary(BaseModel):
    """Current air quality status summary for a selected location."""
    location_name: str = Field(..., description="Name of the city or monitoring area")
    aqi: int = Field(..., description="Current calculated or simulated AQI value")
    category: str = Field(..., description="Severity category (Good, Moderate, Poor, etc.)")
    primary_pollutant: str = Field(default="PM2.5", description="Dominant air pollutant")
    health_advice: str = Field(default="", description="Advisory text based on severity")
    change_rate: Optional[str] = Field(default="+0% from 1hr ago", description="Hour-over-hour trend")
    is_demo: bool = Field(default=True, description="Indicator for simulated/scaffold data")


class ForecastPoint(BaseModel):
    """Single time-step predicted AQI value."""
    hour_label: str = Field(..., description="Hour label (e.g. '02:00', '+6h')")
    predicted_aqi: int = Field(..., description="Forecast AQI value")
    category: str = Field(..., description="Predicted severity category")
    confidence: Optional[float] = Field(default=0.85, description="Model confidence estimate (0-1)")


class StationLocation(BaseModel):
    """Geographic monitoring station representation."""
    station_id: str
    station_name: str
    latitude: float
    longitude: float
    aqi: int
    category: str
    main_pollutant: str
