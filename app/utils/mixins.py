from datetime import datetime

from pydantic import BaseModel, Field


class CreateDateTimeMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UpdateDateTimeMixin(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.utcnow)
