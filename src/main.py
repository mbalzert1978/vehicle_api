"""Vehicle api main module."""
from fastapi import FastAPI

from src.api.v1.endpoints.service_health import service
from src.api.v1.endpoints.vehicle import router
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json",
)

app.include_router(router)
app.include_router(service)
