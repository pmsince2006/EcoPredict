"""Health check routes for service monitoring and data provenance introspection."""

from fastapi import APIRouter
from app.core.config import settings
from app.schemas.aqi import HealthResponse
from app.services.model_service import ModelService

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def get_health_status():
    """Returns application status, version, checkpoint phase, and model provenance."""
    model_service = ModelService.get_instance()

    return HealthResponse(
        status="healthy",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        checkpoint="Checkpoint 3 — Safe Backend Inference & Integration",
        data_status="demo_preview" if model_service.is_demo_model else "real_data_forecast",
        model_loaded=model_service.is_loaded,
        model_provenance=model_service.training_provenance if model_service.is_loaded else None,
        real_data_validated=model_service.real_data_validated,
        environment=settings.ENVIRONMENT,
        disclaimer="DEMO PREVIEW: Inference active using baseline Random Forest trained on synthetic fixture. Real CPCB telemetry pending validation."
        if model_service.is_demo_model
        else "VALIDATED: Production model trained and evaluated against real monitoring observations.",
    )
