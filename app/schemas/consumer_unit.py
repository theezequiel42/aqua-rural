import uuid

from app.schemas.base import SchemaBase, TimestampedReadSchema


class ConsumerUnitCreate(SchemaBase):
    code: str
    customer_id: uuid.UUID
    location_id: uuid.UUID
    default_tariff_plan_id: uuid.UUID | None = None
    status: str = "active"
    notes: str | None = None


class ConsumerUnitRead(TimestampedReadSchema, ConsumerUnitCreate):
    pass
