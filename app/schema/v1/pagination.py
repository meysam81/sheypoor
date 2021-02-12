from pydantic import BaseModel

from .ads import AdOut


class _BasePagination(BaseModel):
    offset: int
    limit: int
    total: int


class PaginatedAd(_BasePagination):
    data: list[AdOut]
