from pydantic import BaseModel

from .mixins import FromAttributesMixin


class SeasonCreateSchema(BaseModel):
    name: str


class SeasonReadSchema(FromAttributesMixin):
    name: str
