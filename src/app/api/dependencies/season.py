from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session_dep import SessionDep, TransactionSessionDep
from app.models.season import Season
from app.repositories.season import SeasonRepository
from app.services.season import SeasonService


async def get_season_service(
    session: Annotated[AsyncSession, SessionDep],
) -> SeasonService:
    repo = SeasonRepository(session, Season)
    return SeasonService(
        session=session,
        repo=repo,
    )


async def get_season_service_tx(
    session: Annotated[AsyncSession, TransactionSessionDep],
) -> SeasonService:
    repo = SeasonRepository(session, Season)
    return SeasonService(
        session=session,
        repo=repo,
    )


SeasonServiceDep = Annotated[SeasonService, Depends(get_season_service)]
SeasonServiceTxDep = Annotated[SeasonService, Depends(get_season_service_tx)]
