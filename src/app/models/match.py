from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import CreatedAtMixin, UpdatedAtMixin, UuidIdMixin

if TYPE_CHECKING:
    from app.models.season import Season


def int_col():
    return mapped_column(Integer, default=0, server_default="0")


class Match(
    Base,
    UuidIdMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
):
    _uuid_primary_key = True
    season: Mapped[str] = mapped_column(ForeignKey("seasons.name"))
    home_team: Mapped[str] = mapped_column(ForeignKey("teams.name"))
    away_team: Mapped[str] = mapped_column(ForeignKey("teams.name"))
    match_date: Mapped[date] = mapped_column(Date)
    referee: Mapped[str] = mapped_column(ForeignKey("referees.name"))
    division: Mapped[str] = mapped_column(ForeignKey("divisions.code"))

    full_time_home_goals: Mapped[int] = mapped_column(Integer)
    full_time_away_goals: Mapped[int] = mapped_column(Integer)
    full_time_result: Mapped[str] = mapped_column(String(10))

    half_time_home_goals: Mapped[int | None] = mapped_column(Integer)
    half_time_away_goals: Mapped[int | None] = mapped_column(Integer)
    half_time_result: Mapped[str | None] = mapped_column(String(10))

    home_shots: Mapped[int] = int_col()
    away_shots: Mapped[int] = int_col()
    home_shots_on_target: Mapped[int] = int_col()
    away_shots_on_target: Mapped[int] = int_col()
    home_fouls: Mapped[int] = int_col()
    away_fouls: Mapped[int] = int_col()
    home_corners: Mapped[int] = int_col()
    away_corners: Mapped[int] = int_col()
    home_yellow_cards: Mapped[int] = int_col()
    away_yellow_cards: Mapped[int] = int_col()
    home_red_cards: Mapped[int] = int_col()
    away_red_cards: Mapped[int] = int_col()

    season_rel: Mapped["Season"] = relationship(
        "Season",
        back_populates="matches",
    )
    __table_args__ = (
        UniqueConstraint(
            "season",
            "home_team",
            "away_team",
            "match_date",
        ),
    )
