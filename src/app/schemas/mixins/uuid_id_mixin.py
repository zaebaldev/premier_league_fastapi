from pydantic import UUID4, BaseModel


class UuidIdMixin(BaseModel):
    id: UUID4
