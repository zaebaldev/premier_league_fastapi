from pydantic import BaseModel

from app.enums.match import MatchResult
from app.schemas.mixins import FromAttributesMixin


class MatchImportReadSchema(BaseModel):
    imported_lines_count: int = 0


class MatchReadSchema(FromAttributesMixin):
    team: str
    total: int
    wins: int
    losses: int
    draws: int
    goals_scored: int
    goals_conceded: int
    goals_difference: int
    score: int
    last_matches: list[MatchResult] | None = None
