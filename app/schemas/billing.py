import uuid
from datetime import date, datetime
from decimal import Decimal

from app.schemas.base import SchemaBase, TimestampedReadSchema


class InvoiceCreate(SchemaBase):
    consumer_unit_id: uuid.UUID
    reading_cycle_id: uuid.UUID | None = None
    issue_date: date
    due_date: date
    status: str = "open"
    total_amount: Decimal
    paid_amount: Decimal = Decimal("0.00")
    notes: str | None = None


class InvoiceRead(TimestampedReadSchema, InvoiceCreate):
    pass


class PaymentCreate(SchemaBase):
    invoice_id: uuid.UUID
    received_by_user_id: uuid.UUID | None = None
    paid_amount: Decimal
    paid_at: datetime
    payment_method: str
    reference: str | None = None
    notes: str | None = None


class PaymentRead(TimestampedReadSchema, PaymentCreate):
    pass
