from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.models.v1.ads import AdBase, AdUpdateBase


class AdIn(AdBase):
    pass


class AdOut(AdBase):
    id: UUID
    contact: str = Field(description="Phone Number", example="+989123456789")
    created_at: datetime
    updated_at: datetime


class AdUpdate(AdUpdateBase):
    pass
