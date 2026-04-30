from sqlalchemy.ext.asyncio import AsyncSession

from app.models.season import Season
from app.repositories.season import SeasonRepository
from app.schemas.season import SeasonReadSchema


class SeasonService:
    def __init__(
        self,
        session: AsyncSession,
        repo: SeasonRepository,
    ):
        self.session = session
        self.repo = repo

    async def get_season_by_name(self, name: str) -> Season | None:
        return await self.repo.get_by_name(name)

    async def get_or_create(self, name: str) -> Season:
        existing = await self.get_season_by_name(name)
        if existing is not None:
            return existing
        season = Season(name=name)
        return await self.repo.add(season)

    async def get_seasons(self) -> list[SeasonReadSchema]:
        rows = await self.repo.get_all()
        return [SeasonReadSchema.model_validate(row) for row in rows]
