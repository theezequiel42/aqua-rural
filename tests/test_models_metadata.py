from app.db.base import Base
from app.models import import_models


EXPECTED_TABLES = {
    "audit_logs",
    "consumer_units",
    "customers",
    "invoice_items",
    "invoices",
    "locations",
    "meter_events",
    "meter_installations",
    "meter_readings",
    "meters",
    "payments",
    "reading_cycles",
    "tariff_plans",
    "tariff_tiers",
    "users",
}


def test_metadata_registers_all_core_tables() -> None:
    import_models()

    assert EXPECTED_TABLES.issubset(Base.metadata.tables.keys())
