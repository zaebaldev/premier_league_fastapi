import csv
import io

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.match import Match
from app.repositories.match import MatchRepository
from app.schemas.match import MatchReadSchema
from app.services.division import DivisionService
from app.services.referee import RefereeService
from app.services.season import SeasonService
from app.services.team import TeamService
from core.utils.parse_date import parse_date


class MatchService:
    def __init__(
        self,
        session: AsyncSession,
        repo: MatchRepository,
        season_service: SeasonService,
        team_service: TeamService,
        referee_service: RefereeService,
        division_service: DivisionService,
    ):
        self.session = session
        self.repo = repo
        self.season_service = season_service
        self.team_service = team_service
        self.referee_service = referee_service
        self.division_service = division_service

    async def import_matches_from_csv(
        self,
        file: UploadFile,
    ) -> int:
        season_name = file.filename.split(".")[0]
        contents = await file.read()
        decoded_contents = contents.decode("utf-8")

        season = await self.season_service.get_or_create(season_name)
        inserted_count = 0

        for row in csv.DictReader(io.StringIO(decoded_contents)):
            await self.referee_service.get_or_create(row.get("Referee"))
            await self.division_service.get_or_create(row["Div"])

            home_team = row["HomeTeam"]
            away_team = row["AwayTeam"]
            await self.team_service.get_or_create(home_team)
            await self.team_service.get_or_create(away_team)

            await self.repo.add(
                Match(
                    season=season.name,
                    home_team=home_team,
                    away_team=away_team,
                    match_date=parse_date(row["Date"]),
                    referee=row["Referee"].strip(),
                    division=row["Div"].strip(),
                    full_time_home_goals=int(row["FTHG"]),
                    full_time_away_goals=int(row["FTAG"]),
                    full_time_result=row["FTR"],
                    half_time_home_goals=int(row["HTHG"]),
                    half_time_away_goals=int(row["HTAG"]),
                    half_time_result=row["HTR"],
                    home_shots=int(row["HS"]),
                    away_shots=int(row["AS"]),
                    home_shots_on_target=int(row["HST"]),
                    away_shots_on_target=int(row["AST"]),
                    home_fouls=int(row["HF"]),
                    away_fouls=int(row["AF"]),
                    home_corners=int(row["HC"]),
                    away_corners=int(row["AC"]),
                    home_yellow_cards=int(row["HY"]),
                    away_yellow_cards=int(row["AY"]),
                    home_red_cards=int(row["HR"]),
                    away_red_cards=int(row["AR"]),
                )
            )
            inserted_count += 1

        await self.session.commit()
        return inserted_count

    async def get_matches(
        self,
        season: str,
        limit: int,
        offset: int,
    ) -> list[MatchReadSchema]:
        rows = await self.repo.get_matches(
            season=season,
            limit=limit,
            offset=offset,
        )
        return [MatchReadSchema.model_validate(dict(row)) for row in rows]
