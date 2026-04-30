from sqlalchemy.ext.asyncio import AsyncSession

from app.models.division import Division
from app.repositories.division import DivisionRepository


class DivisionService:
    def __init__(
        self,
        session: AsyncSession,
        repo: DivisionRepository,
    ):
        self.session = session
        self.repo = repo

    async def get(
        self,
        code: str,
    ) -> Division | None:
        return await self.repo.get_by_id(code)

    async def get_or_create(
        self,
        code: str,
    ) -> Division:
        return await self.repo.get_or_create(
            filters=[Division.code == code],
            create_values={
                "code": code,
            },
        )
