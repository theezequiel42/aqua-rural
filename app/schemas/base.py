from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampedReadSchema(SchemaBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
