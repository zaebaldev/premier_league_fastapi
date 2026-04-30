from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.referee import Referee

from .base import BaseRepository


class RefereeRepository(BaseRepository[Referee]):
    def __init__(
        self,
        session: AsyncSession,
        model: Type[Referee],
    ):
        super().__init__(session, model)
