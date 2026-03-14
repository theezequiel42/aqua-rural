from datetime import date
from decimal import Decimal

from pydantic import Field

from app.schemas.base import SchemaBase, TimestampedReadSchema


class TariffTierCreate(SchemaBase):
    consumption_from: int
    consumption_to: int | None = None
    unit_price: Decimal
    fixed_fee: Decimal = Decimal("0.00")


class TariffTierRead(TimestampedReadSchema, TariffTierCreate):
    pass


class TariffPlanCreate(SchemaBase):
    name: str
    description: str | None = None
    effective_start_date: date
    effective_end_date: date | None = None
    is_active: bool = True


class TariffPlanRead(TimestampedReadSchema, TariffPlanCreate):
    tariff_tiers: list[TariffTierRead] = Field(default_factory=list)
