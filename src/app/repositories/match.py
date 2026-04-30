from typing import Any, Mapping, Type

from sqlalchemy import case, func, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.match import MatchResult
from app.models.match import Match

from .base import BaseRepository

LAST_MATCHES_COUNT = 5


class MatchRepository(BaseRepository[Match]):
    def __init__(
        self,
        session: AsyncSession,
        model: Type[Match],
    ):
        super().__init__(session, model)

    async def get_matches(
        self,
        season: str,
        limit: int,
        offset: int,
    ) -> list[Mapping[str, Any]]:
        home_team = select(
            Match.match_date,
            Match.home_team.label("team"),
            Match.full_time_home_goals.label("goals_scored"),
            Match.full_time_away_goals.label("goals_conceded"),
            Match.full_time_result.label("team_result"),
        ).where(Match.season == season)

        away_team = select(
            Match.match_date,
            Match.away_team.label("team"),
            Match.full_time_away_goals.label("goals_scored"),
            Match.full_time_home_goals.label("goals_conceded"),
            case(
                (Match.full_time_result == MatchResult.HOME_WIN, MatchResult.AWAY_WIN),
                (Match.full_time_result == MatchResult.AWAY_WIN, MatchResult.HOME_WIN),
                else_=MatchResult.DRAW,
            ).label("team_result"),
        ).where(Match.season == season)

        team_matches = union_all(home_team, away_team).subquery()

        wins_count = func.sum(
            case((team_matches.c.team_result == MatchResult.HOME_WIN, 1), else_=0)
        )
        losses_count = func.sum(
            case((team_matches.c.team_result == MatchResult.AWAY_WIN, 1), else_=0)
        )
        draws_count = func.sum(
            case((team_matches.c.team_result == MatchResult.DRAW, 1), else_=0)
        )
        goals_scored = func.sum(team_matches.c.goals_scored)
        goals_conceded = func.sum(team_matches.c.goals_conceded)
        score = wins_count * 3 + draws_count
        ranked = select(
            team_matches.c.team,
            team_matches.c.team_result,
            team_matches.c.match_date,
            func.row_number()
            .over(
                partition_by=team_matches.c.team,
                order_by=team_matches.c.match_date.desc(),
            )
            .label("rn"),
        ).subquery()
        last_matches = (
            select(
                ranked.c.team,
                func.array_agg(ranked.c.team_result).label("last_matches"),
            )
            .where(ranked.c.rn <= LAST_MATCHES_COUNT)
            .group_by(ranked.c.team)
        ).subquery()
        stmt = (
            select(
                team_matches.c.team.label("team"),
                func.count().label("total"),
                wins_count.label("wins"),
                losses_count.label("losses"),
                draws_count.label("draws"),
                goals_scored.label("goals_scored"),
                goals_conceded.label("goals_conceded"),
                (goals_scored - goals_conceded).label("goals_difference"),
                score.label("score"),
                last_matches.c.last_matches.label("last_matches"),
            )
            .group_by(
                team_matches.c.team,
                last_matches.c.last_matches,
            )
            .order_by(
                score.desc(),
                (goals_scored - goals_conceded).desc(),
                goals_scored.desc(),
            )
            .join(last_matches, team_matches.c.team == last_matches.c.team)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()
