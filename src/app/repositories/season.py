from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.season import Season

from .base import BaseRepository


class SeasonRepository(BaseRepository[Season]):
    def __init__(
        self,
        session: AsyncSession,
        model: Type[Season],
    ):
        super().__init__(session, model)

    async def get_or_create(self, name: str) -> Season:
        existing = await self.get_by_id(name)
        if existing is not None:
            return existing
        return await self.add(Season(name=name))

    async def get_by_name(self, name: str) -> Season | None:
        stmt = select(Season).where(Season.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
