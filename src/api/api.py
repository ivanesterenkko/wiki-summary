from fastapi import APIRouter

from src.api.endpoints.wiki import router as endpoint_router

router = APIRouter()

router.include_router(endpoint_router)
