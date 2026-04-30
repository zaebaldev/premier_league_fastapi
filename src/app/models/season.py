from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .mixins import CreatedAtMixin, NameMixin

if TYPE_CHECKING:
    from models.match import Match


class Season(
    Base,
    CreatedAtMixin,
    NameMixin,
):
    _name_primary_key = True
    _name_unique = True
    matches: Mapped[list["Match"]] = relationship(
        "Match",
        back_populates="season_rel",
        cascade="all, delete-orphan",
    )
