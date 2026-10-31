"""Application settings and configuration module."""

import os
from pathlib import Path
from typing import List


class Settings:
    """Core application settings with environment variable support."""

    PROJECT_NAME: str = "EcoPredict API"
    VERSION: str = "0.3.0-checkpoint3"
    DESCRIPTION: str = (
        "EcoPredict Backend API — Air Quality Monitoring & AQI Forecasting Service"
    )
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1")

    # API Prefix
    API_V1_PREFIX: str = "/api"

    # Repository Root Anchor (avoids dependency on arbitrary current working directory)
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent

    # Model Artifacts Directory (anchored to PROJECT_ROOT/ml/models by default)
    _env_model_dir = os.getenv("MODEL_ARTIFACTS_DIR", "ml/models")
    MODEL_ARTIFACTS_DIR: Path = (
        Path(_env_model_dir)
        if Path(_env_model_dir).is_absolute()
        else PROJECT_ROOT / _env_model_dir
    )

    DEFAULT_MODEL_NAME: str = os.getenv("DEFAULT_MODEL_NAME", "baseline_random_forest.pkl")
    DEFAULT_METADATA_NAME: str = os.getenv("DEFAULT_METADATA_NAME", "model_metadata.json")

    # Data Status: 'real_observation' | 'real_data_forecast' | 'demo_preview' | 'unavailable'
    DEFAULT_DATA_STATUS: str = "demo_preview"

    # CORS configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


settings = Settings()
