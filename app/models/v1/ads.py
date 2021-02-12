from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.utils.mixins import CreateDateTimeMixin, UpdateDateTimeMixin


class AdBase(BaseModel):
    title: str
    description: Optional[str] = Field(max_length=512)
    address: str


class AdDBWrite(AdBase, CreateDateTimeMixin, UpdateDateTimeMixin):
    id: UUID = Field(default_factory=uuid4)
    contact: str = Field(description="Phone Number", example="+989123456789")


class AdDBRead(AdBase):
    id: UUID
    contact: str = Field(description="Phone Number", example="+989123456789")
    created_at: datetime
    updated_at: datetime


class AdUpdateBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    address: Optional[str]


class AdQuery(BaseModel):
    id: Optional[UUID]


class AdUpdateDB(AdUpdateBase, UpdateDateTimeMixin):
    pass
