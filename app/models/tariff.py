from __future__ import annotations

from datetime import date
from decimal import Decimal
import uuid

from sqlalchemy import Boolean, CheckConstraint, Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampedUUIDMixin


class TariffPlan(TimestampedUUIDMixin, Base):
    __tablename__ = "tariff_plans"
    __table_args__ = (
        CheckConstraint(
            "effective_end_date IS NULL OR effective_end_date >= effective_start_date",
            name="valid_tariff_plan_date_range",
        ),
    )

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    effective_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    effective_end_date: Mapped[date | None] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tariff_tiers = relationship("TariffTier", back_populates="tariff_plan", cascade="all, delete-orphan")
    consumer_units = relationship("ConsumerUnit", back_populates="default_tariff_plan")


class TariffTier(TimestampedUUIDMixin, Base):
    __tablename__ = "tariff_tiers"
    __table_args__ = (
        CheckConstraint("consumption_to IS NULL OR consumption_to >= consumption_from", name="valid_tariff_tier_range"),
    )

    tariff_plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tariff_plans.id"), nullable=False)
    consumption_from: Mapped[int] = mapped_column(nullable=False)
    consumption_to: Mapped[int | None] = mapped_column()
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    fixed_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    tariff_plan = relationship("TariffPlan", back_populates="tariff_tiers")
