import uuid
from datetime import datetime
from decimal import Decimal

from app.schemas.base import SchemaBase, TimestampedReadSchema


class MeterCreate(SchemaBase):
    serial_number: str
    manufacturer: str | None = None
    model_name: str | None = None
    status: str = "available"


class MeterRead(TimestampedReadSchema, MeterCreate):
    pass


class MeterReadingCreate(SchemaBase):
    consumer_unit_id: uuid.UUID
    meter_id: uuid.UUID
    reading_cycle_id: uuid.UUID
    created_by_user_id: uuid.UUID | None = None
    previous_reading: Decimal
    current_reading: Decimal
    measured_consumption: Decimal
    read_at: datetime
    source: str = "manual"
    notes: str | None = None


class MeterReadingRead(TimestampedReadSchema, MeterReadingCreate):
    pass
