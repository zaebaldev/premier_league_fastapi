from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session_dep import SessionDep, TransactionSessionDep
from app.models.division import Division
from app.models.match import Match
from app.models.referee import Referee
from app.models.season import Season
from app.models.team import Team
from app.repositories.division import DivisionRepository
from app.repositories.match import MatchRepository
from app.repositories.referee import RefereeRepository
from app.repositories.season import SeasonRepository
from app.repositories.team import TeamRepository
from app.services.division import DivisionService
from app.services.match import MatchService
from app.services.referee import RefereeService
from app.services.season import SeasonService
from app.services.team import TeamService


async def get_match_service(
    session: Annotated[AsyncSession, SessionDep],
) -> MatchService:
    repo = MatchRepository(session, Match)
    season_repo = SeasonRepository(session, Season)
    team_repo = TeamRepository(session, Team)
    referee_repo = RefereeRepository(session, Referee)
    division_repo = DivisionRepository(session, Division)
    return MatchService(
        session=session,
        repo=repo,
        season_service=SeasonService(session, season_repo),
        team_service=TeamService(session, team_repo),
        referee_service=RefereeService(session, referee_repo),
        division_service=DivisionService(session, division_repo),
    )


async def get_match_service_tx(
    session: Annotated[AsyncSession, TransactionSessionDep],
) -> MatchService:
    repo = MatchRepository(session, Match)
    season_repo = SeasonRepository(session, Season)
    team_repo = TeamRepository(session, Team)
    referee_repo = RefereeRepository(session, Referee)
    division_repo = DivisionRepository(session, Division)
    return MatchService(
        session=session,
        repo=repo,
        season_service=SeasonService(session, season_repo),
        team_service=TeamService(session, team_repo),
        referee_service=RefereeService(session, referee_repo),
        division_service=DivisionService(session, division_repo),
    )


MatchServiceDep = Annotated[MatchService, Depends(get_match_service)]
MatchServiceTxDep = Annotated[MatchService, Depends(get_match_service_tx)]
