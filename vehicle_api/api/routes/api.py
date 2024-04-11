from fastapi import APIRouter

from vehicle_api.api.routes import service_health, vehicle

router = APIRouter()
router.include_router(service_health.router, tags=["service health"], prefix="/service")
router.include_router(vehicle.router, tags=["vehicles"], prefix="/vehicles")
