"""Pydantic data models for Air Quality metrics, forecasts, monitoring stations, and health."""

from typing import List, Optional, Literal
from datetime import datetime, timezone
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(*args, **kwargs):
        return kwargs.get("default", None)

DataStatusType = Literal["real_observation", "real_data_forecast", "demo_preview", "unavailable"]


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
    severity_color: str = Field(default="#f97316", description="Hex color token for category")
    primary_pollutant: str = Field(default="PM2.5", description="Dominant air pollutant")
    primary_concentration: str = Field(default="92 µg/m³", description="Concentration of primary pollutant")
    twelve_hour_prediction: int = Field(default=164, description="12-hour projected AQI index")
    twelve_hour_category: str = Field(default="Poor", description="Projected severity category")
    prediction_confidence: str = Field(default="88%", description="Model confidence indicator")
    health_advice: str = Field(default="", description="Advisory text based on severity")
    change_rate: str = Field(default="+0% from 1hr ago", description="Hour-over-hour trend")
    data_status: str = Field(default="demo_preview", description="Provenance status: real_observation or demo_preview")
    is_demo_data: bool = Field(default=True, description="Explicit boolean flag for synthetic/scaffold data")
    pollutants: PollutantMetrics = Field(default_factory=PollutantMetrics)
    last_updated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class StationLocation(BaseModel):
    """Geographic monitoring station representation."""
    id: str = Field(..., description="Unique station identifier")
    name: str = Field(..., description="Human-readable station name")
    lat: float = Field(..., description="Latitude coordinate")
    lng: float = Field(..., description="Longitude coordinate")
    aqi: int = Field(..., description="Current station AQI reading")
    category: str = Field(..., description="Severity category")
    status: str = Field(default="Active", description="Station operational status")
    main_pollutant: str = Field(default="PM 2.5", description="Primary pollutant concentration")


class StationResponse(BaseModel):
    """Response envelope for monitoring station telemetry."""
    stations: List[StationLocation] = Field(default_factory=list)
    data_status: str = Field(default="demo_preview")
    is_demo_data: bool = Field(default=True)
    count: int = Field(default=0)


class ForecastPoint(BaseModel):
    """Single forward time-step predicted value."""
    time: str = Field(..., description="Timestamp or hour label (e.g. '02:00', '+1h')")
    predicted_pm25: float = Field(..., description="Predicted continuous PM2.5 in µg/m³")
    predicted_aqi: int = Field(..., description="Mapped CPCB AQI value")
    lower_bound_pm25: float = Field(..., description="Lower 85% confidence bound (µg/m³)")
    upper_bound_pm25: float = Field(..., description="Upper 85% confidence bound (µg/m³)")
    category: str = Field(..., description="Predicted severity category")


class ForecastResponse(BaseModel):
    """Response envelope for model forecast queries."""
    target_variable: str = Field(default="pm25", description="Target environmental pollutant")
    target_unit: str = Field(default="µg/m³", description="Physical unit of measurement")
    forecast_horizon_hours: int = Field(default=1, description="Forward forecast horizon in hours")
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    location_name: str = Field(default="Delhi NCR", description="Forecast geographic region")
    station_id: Optional[str] = Field(default=None, description="Station ID if single-station forecast")
    data_status: str = Field(default="demo_preview", description="'real_data_forecast' | 'demo_preview' | 'unavailable'")
    is_demo_model: bool = Field(default=True, description="True if model was trained on synthetic fixture")
    real_data_validated: bool = Field(default=False, description="True ONLY when trained on real CPCB data")
    model_version: Optional[str] = Field(default="0.2.0-baseline-rf")
    model_provenance: Optional[str] = Field(default="synthetic_fixture")
    model_mae: Optional[float] = Field(default=None)
    model_rmse: Optional[float] = Field(default=None)
    forecast_points: List[ForecastPoint] = Field(default_factory=list)
    disclaimer: str = Field(
        default="DEMO PREVIEW: Output generated from baseline Random Forest trained on synthetic test fixture. Not validated against real CPCB observations."
    )


class HealthResponse(BaseModel):
    """System health check and data provenance response."""
    status: str = Field(default="healthy")
    service: str = Field(default="EcoPredict Backend API")
    version: str = Field(default="0.3.0-checkpoint3")
    checkpoint: str = Field(default="Checkpoint 3 — Safe Backend Inference & Integration")
    data_status: str = Field(default="demo_preview")
    model_loaded: bool = Field(default=False)
    model_provenance: Optional[str] = Field(default=None)
    real_data_validated: bool = Field(default=False)
    environment: str = Field(default="development")
    disclaimer: str = Field(
        default="DEMO PREVIEW: Backend inference is active using synthetic baseline model. Real CPCB data validation pending."
    )
