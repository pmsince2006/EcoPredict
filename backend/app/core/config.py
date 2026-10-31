"""Application settings and configuration module."""
import os
from typing import List


class Settings:
    """Core application settings with environment variable support."""

    PROJECT_NAME: str = "EcoPredict API"
    VERSION: str = "0.1.0-checkpoint1"
    DESCRIPTION: str = (
        "EcoPredict Backend API — Air Quality Monitoring & AQI Forecasting Scaffold"
    )
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")

    # API Prefix
    API_V1_PREFIX: str = "/api"

    # CORS configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]


settings = Settings()
