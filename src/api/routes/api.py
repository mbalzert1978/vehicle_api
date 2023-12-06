from fastapi import APIRouter

from src.api.routes import service_health, vehicle

router = APIRouter()
router.include_router(service_health.router, tags=["service health"], prefix="/service")
router.include_router(vehicle.router, tags=["vehicle"], prefix="/vehicle")
