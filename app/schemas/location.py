from decimal import Decimal

from app.schemas.base import SchemaBase, TimestampedReadSchema


class LocationCreate(SchemaBase):
    label: str
    rural_community: str | None = None
    address_line: str | None = None
    address_details: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class LocationRead(TimestampedReadSchema, LocationCreate):
    pass
