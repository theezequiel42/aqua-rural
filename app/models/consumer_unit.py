from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampedUUIDMixin


class ConsumerUnit(TimestampedUUIDMixin, Base):
    __tablename__ = "consumer_units"

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("customers.id"), nullable=False)
    location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id"), nullable=False)
    default_tariff_plan_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("tariff_plans.id"))
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    customer = relationship("Customer", back_populates="consumer_units")
    location = relationship("Location", back_populates="consumer_units")
    default_tariff_plan = relationship("TariffPlan", back_populates="consumer_units")
    meter_installations = relationship("MeterInstallation", back_populates="consumer_unit", cascade="all, delete-orphan")
    meter_readings = relationship("MeterReading", back_populates="consumer_unit", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="consumer_unit", cascade="all, delete-orphan")
    meter_events = relationship("MeterEvent", back_populates="consumer_unit", cascade="all, delete-orphan")
