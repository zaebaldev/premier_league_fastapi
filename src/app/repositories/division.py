from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.division import Division

from .base import BaseRepository


class DivisionRepository(BaseRepository[Division]):
    def __init__(
        self,
        session: AsyncSession,
        model: Type[Division],
    ):
        super().__init__(session, model)
