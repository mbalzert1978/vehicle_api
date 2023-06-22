from fastapi import FastAPI

from src.api.v1.endpoints.vehicle import router
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json",
)


app.include_router(router)
