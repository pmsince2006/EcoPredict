"""EcoPredict Backend Application Entrypoint.

Provides FastAPI app initialization, middleware, CORS setup, and route registration.
"""

import sys
from pathlib import Path

# Ensure app package is resolvable regardless of run location
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


def create_application():
    """Application factory for EcoPredict backend."""
    if not FASTAPI_AVAILABLE:
        # Fallback dummy callable when running without FastAPI installed
        class DummyApp:
            def __call__(self, *args, **kwargs):
                pass
        return DummyApp()

    from app.core.config import settings
    from app.api.routes import health, aqi

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Enable CORS for frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    app.include_router(health.router, prefix=settings.API_V1_PREFIX)
    app.include_router(aqi.router, prefix=settings.API_V1_PREFIX)

    @app.get("/")
    def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "status": "online",
            "docs": "/docs",
        }

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
