from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import uuid

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampedUUIDMixin


class Meter(TimestampedUUIDMixin, Base):
    __tablename__ = "meters"

    serial_number: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    manufacturer: Mapped[str | None] = mapped_column(String(120))
    model_name: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(30), default="available", nullable=False)

    installations = relationship("MeterInstallation", back_populates="meter", cascade="all, delete-orphan")
    readings = relationship("MeterReading", back_populates="meter")
    events = relationship("MeterEvent", back_populates="meter", cascade="all, delete-orphan")


class MeterInstallation(TimestampedUUIDMixin, Base):
    __tablename__ = "meter_installations"
    __table_args__ = (
        CheckConstraint("removed_at IS NULL OR removed_at >= installed_at", name="valid_installation_period"),
    )

    consumer_unit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("consumer_units.id"), nullable=False)
    meter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meters.id"), nullable=False)
    installed_by_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    installed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    removed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text)

    consumer_unit = relationship("ConsumerUnit", back_populates="meter_installations")
    meter = relationship("Meter", back_populates="installations")
    installed_by_user = relationship("User", back_populates="meter_installations")


class ReadingCycle(TimestampedUUIDMixin, Base):
    __tablename__ = "reading_cycles"
    __table_args__ = (UniqueConstraint("reference_month", name="uq_reading_cycles_reference_month"),)

    reference_month: Mapped[date] = mapped_column(Date, nullable=False)
    starts_on: Mapped[date] = mapped_column(Date, nullable=False)
    ends_on: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open", nullable=False)

    readings = relationship("MeterReading", back_populates="reading_cycle")
    invoices = relationship("Invoice", back_populates="reading_cycle")


class MeterReading(TimestampedUUIDMixin, Base):
    __tablename__ = "meter_readings"
    __table_args__ = (
        UniqueConstraint("consumer_unit_id", "reading_cycle_id", name="uq_meter_reading_consumer_unit_cycle"),
        CheckConstraint("current_reading >= previous_reading", name="meter_reading_not_decreasing"),
    )

    consumer_unit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("consumer_units.id"), nullable=False)
    meter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meters.id"), nullable=False)
    reading_cycle_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reading_cycles.id"), nullable=False)
    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    previous_reading: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    current_reading: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    measured_consumption: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source: Mapped[str] = mapped_column(String(30), default="manual", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    consumer_unit = relationship("ConsumerUnit", back_populates="meter_readings")
    meter = relationship("Meter", back_populates="readings")
    reading_cycle = relationship("ReadingCycle", back_populates="readings")
    created_by_user = relationship("User", back_populates="created_readings")


class MeterEvent(TimestampedUUIDMixin, Base):
    __tablename__ = "meter_events"

    meter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meters.id"), nullable=False)
    consumer_unit_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("consumer_units.id"))
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    meter = relationship("Meter", back_populates="events")
    consumer_unit = relationship("ConsumerUnit", back_populates="meter_events")
