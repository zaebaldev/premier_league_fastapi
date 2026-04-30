from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team
from app.repositories.team import TeamRepository


class TeamService:
    def __init__(
        self,
        session: AsyncSession,
        repo: TeamRepository,
    ):
        self.session = session
        self.repo = repo

    async def get(
        self,
        name: str,
    ) -> Team | None:
        return await self.repo.get_by_id(name)

    async def get_or_create(
        self,
        name: str,
    ) -> Team:
        return await self.repo.get_or_create(
            filters=[Team.name == name],
            create_values={
                "name": name,
            },
        )
