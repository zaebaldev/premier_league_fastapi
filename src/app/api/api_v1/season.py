from fastapi import APIRouter

from app.api.dependencies.season import SeasonServiceDep, SeasonServiceTxDep
from app.schemas.season import SeasonCreateSchema, SeasonReadSchema
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.seasons,
    tags=["Seasons"],
)


@router.post(
    "",
    response_model=SeasonReadSchema,
)
async def create_season(
    service: SeasonServiceTxDep,
    data: SeasonCreateSchema,
):
    return await service.get_or_create(
        name=data.name,
    )


@router.get(
    "",
    response_model=list[SeasonReadSchema],
)
async def get_seasons(
    service: SeasonServiceDep,
):
    return await service.get_seasons()
