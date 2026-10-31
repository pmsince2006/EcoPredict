"""Health check routes for service monitoring."""
try:
    from fastapi import APIRouter
except ImportError:
    class APIRouter:
        def __init__(self, *args, **kwargs):
            pass
        def get(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

router = APIRouter(tags=["Health"])


@router.get("/health")
def get_health_status():
    """Returns application status, version, and checkpoint phase."""
    return {
        "status": "healthy",
        "service": "EcoPredict Backend API",
        "checkpoint": "Checkpoint 1 — Project Foundation",
        "mock_mode": True,
    }
