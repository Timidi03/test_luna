from fastapi.routing import APIRouter

from src.api.v1.organization import router as organization_router

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(
    organization_router, prefix="/organizations", tags=["organizations"]
)
