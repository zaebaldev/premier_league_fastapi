from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import CreatedAtMixin, NameMixin

if TYPE_CHECKING:
    pass


class Division(
    Base,
    CreatedAtMixin,
    NameMixin,
):
    _name_primary_key = False
    _name_nullable = True
    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        primary_key=True,
        nullable=False,
        index=True,
    )
