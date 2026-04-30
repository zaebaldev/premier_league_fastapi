from typing import TYPE_CHECKING

from .base import Base
from .mixins import CreatedAtMixin, NameMixin

if TYPE_CHECKING:
    pass


class Referee(
    Base,
    CreatedAtMixin,
    NameMixin,
):
    _name_unique = True
