from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampedUUIDMixin


class Location(TimestampedUUIDMixin, Base):
    __tablename__ = "locations"

    label: Mapped[str] = mapped_column(String(255), nullable=False)
    rural_community: Mapped[str | None] = mapped_column(String(255))
    address_line: Mapped[str | None] = mapped_column(String(255))
    address_details: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(String(120))
    state: Mapped[str | None] = mapped_column(String(120))
    postal_code: Mapped[str | None] = mapped_column(String(20))
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))

    consumer_units = relationship("ConsumerUnit", back_populates="location")
