from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team

from .base import BaseRepository


class TeamRepository(BaseRepository[Team]):
    def __init__(
        self,
        session: AsyncSession,
        model: Type[Team],
    ):
        super().__init__(session, model)
