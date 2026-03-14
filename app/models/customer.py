from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampedUUIDMixin


class Customer(TimestampedUUIDMixin, Base):
    __tablename__ = "customers"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    document_number: Mapped[str | None] = mapped_column(String(32), unique=True)
    email: Mapped[str | None] = mapped_column(String(255))
    phone_number: Mapped[str | None] = mapped_column(String(32))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    consumer_units = relationship("ConsumerUnit", back_populates="customer")
