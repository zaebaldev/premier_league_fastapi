from fastapi import APIRouter

from core.config import settings

from .match import router as match_router
from .season import router as season_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(season_router)
router.include_router(match_router)
