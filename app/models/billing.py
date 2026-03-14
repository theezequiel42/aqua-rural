from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import uuid

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampedUUIDMixin


class Invoice(TimestampedUUIDMixin, Base):
    __tablename__ = "invoices"
    __table_args__ = (
        UniqueConstraint("consumer_unit_id", "reading_cycle_id", name="uq_invoice_consumer_unit_cycle"),
        CheckConstraint("paid_amount <= total_amount", name="invoice_paid_amount_not_above_total"),
    )

    consumer_unit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("consumer_units.id"), nullable=False)
    reading_cycle_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("reading_cycles.id"))
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open", nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    consumer_unit = relationship("ConsumerUnit", back_populates="invoices")
    reading_cycle = relationship("ReadingCycle", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(TimestampedUUIDMixin, Base):
    __tablename__ = "invoice_items"

    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), default=1, nullable=False)
    unit_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    invoice = relationship("Invoice", back_populates="items")


class Payment(TimestampedUUIDMixin, Base):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("paid_amount > 0", name="payment_positive_amount"),
    )

    invoice_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    received_by_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    reference: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text)

    invoice = relationship("Invoice", back_populates="payments")
    received_by_user = relationship("User", back_populates="received_payments")
