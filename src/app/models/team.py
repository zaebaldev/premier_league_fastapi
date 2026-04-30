from typing import TYPE_CHECKING

from .base import Base
from .mixins import CreatedAtMixin, NameMixin

if TYPE_CHECKING:
    pass


class Team(
    Base,
    CreatedAtMixin,
    NameMixin,
):
    _name_primary_key = True
    _name_unique = True
