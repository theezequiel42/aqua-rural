from __future__ import annotations

import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampedUUIDMixin


class User(TimestampedUUIDMixin, Base):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_readings = relationship("MeterReading", back_populates="created_by_user")
    meter_installations = relationship("MeterInstallation", back_populates="installed_by_user")
    received_payments = relationship("Payment", back_populates="received_by_user")
    audit_logs = relationship("AuditLog", back_populates="user")
