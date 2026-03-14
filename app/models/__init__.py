from app.models.audit import AuditLog
from app.models.billing import Invoice, InvoiceItem, Payment
from app.models.consumer_unit import ConsumerUnit
from app.models.customer import Customer
from app.models.location import Location
from app.models.meter import Meter, MeterEvent, MeterInstallation, MeterReading, ReadingCycle
from app.models.tariff import TariffPlan, TariffTier
from app.models.user import User


def import_models() -> None:
    """Import models for metadata registration."""


__all__ = [
    "AuditLog",
    "ConsumerUnit",
    "Customer",
    "Invoice",
    "InvoiceItem",
    "Location",
    "Meter",
    "MeterEvent",
    "MeterInstallation",
    "MeterReading",
    "Payment",
    "ReadingCycle",
    "TariffPlan",
    "TariffTier",
    "User",
    "import_models",
]
