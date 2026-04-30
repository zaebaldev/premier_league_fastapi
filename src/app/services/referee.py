from sqlalchemy.ext.asyncio import AsyncSession

from app.models.referee import Referee
from app.repositories.referee import RefereeRepository


class RefereeService:
    def __init__(
        self,
        session: AsyncSession,
        repo: RefereeRepository,
    ):
        self.session = session
        self.repo = repo

    async def get(self, name: str) -> Referee | None:
        return await self.repo.get_by_id(name.strip())

    async def get_or_create(self, name: str) -> Referee:
        return await self.repo.get_or_create(
            filters=[Referee.name == name],
            create_values={
                "name": name,
            },
        )
