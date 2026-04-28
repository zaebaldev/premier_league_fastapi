from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class UuidIdMixin:
    _uuid_primary_key: bool = True

    @declared_attr
    def id(cls) -> Mapped[UUID]:
        return mapped_column(
            PGUUID(as_uuid=True),
            primary_key=cls._uuid_primary_key,
            default=uuid4,
        )
