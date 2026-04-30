from fastapi import APIRouter, File, Query, UploadFile, status

from app.api.dependencies.match import MatchServiceDep
from app.schemas.match import MatchImportReadSchema, MatchReadSchema
from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.matches,
    tags=["Matches"],
)


@router.post(
    "/import",
    response_model=MatchImportReadSchema,
    status_code=status.HTTP_200_OK,
)
async def import_matches_from_csv(
    service: MatchServiceDep,
    file: UploadFile = File(...),
):
    lines = await service.import_matches_from_csv(file)
    return MatchImportReadSchema(
        imported_lines_count=lines,
    )


@router.get(
    "",
    response_model=list[MatchReadSchema],
)
async def get_matches(
    service: MatchServiceDep,
    season: str = Query(...),
    limit: int = Query(default=5),
    offset: int = Query(default=0),
):
    return await service.get_matches(
        season=season,
        limit=limit,
        offset=offset,
    )
