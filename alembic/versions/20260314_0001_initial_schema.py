"""Initial AquaRural schema."""

from alembic import op
import sqlalchemy as sa

revision = "20260314_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("document_number", sa.String(length=32), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone_number", sa.String(length=32), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_customers")),
        sa.UniqueConstraint("document_number", name=op.f("uq_customers_document_number")),
    )
    op.create_table(
        "locations",
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("rural_community", sa.String(length=255), nullable=True),
        sa.Column("address_line", sa.String(length=255), nullable=True),
        sa.Column("address_details", sa.Text(), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("state", sa.String(length=120), nullable=True),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column("latitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_locations")),
    )
    op.create_table(
        "meters",
        sa.Column("serial_number", sa.String(length=80), nullable=False),
        sa.Column("manufacturer", sa.String(length=120), nullable=True),
        sa.Column("model_name", sa.String(length=120), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meters")),
        sa.UniqueConstraint("serial_number", name=op.f("uq_meters_serial_number")),
    )
    op.create_table(
        "reading_cycles",
        sa.Column("reference_month", sa.Date(), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=False),
        sa.Column("ends_on", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reading_cycles")),
        sa.UniqueConstraint("reference_month", name="uq_reading_cycles_reference_month"),
    )
    op.create_table(
        "tariff_plans",
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("effective_start_date", sa.Date(), nullable=False),
        sa.Column("effective_end_date", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "effective_end_date IS NULL OR effective_end_date >= effective_start_date",
            name="valid_tariff_plan_date_range",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tariff_plans")),
    )
    op.create_table(
        "users",
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_table(
        "audit_logs",
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("entity_name", sa.String(length=120), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("logged_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_audit_logs_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_logs")),
    )
    op.create_table(
        "consumer_units",
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("location_id", sa.Uuid(), nullable=False),
        sa.Column("default_tariff_plan_id", sa.Uuid(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], name=op.f("fk_consumer_units_customer_id_customers")),
        sa.ForeignKeyConstraint(["default_tariff_plan_id"], ["tariff_plans.id"], name=op.f("fk_consumer_units_default_tariff_plan_id_tariff_plans")),
        sa.ForeignKeyConstraint(["location_id"], ["locations.id"], name=op.f("fk_consumer_units_location_id_locations")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_consumer_units")),
        sa.UniqueConstraint("code", name=op.f("uq_consumer_units_code")),
    )
    op.create_table(
        "meter_events",
        sa.Column("meter_id", sa.Uuid(), nullable=False),
        sa.Column("consumer_unit_id", sa.Uuid(), nullable=True),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["consumer_unit_id"], ["consumer_units.id"], name=op.f("fk_meter_events_consumer_unit_id_consumer_units")),
        sa.ForeignKeyConstraint(["meter_id"], ["meters.id"], name=op.f("fk_meter_events_meter_id_meters")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meter_events")),
    )
    op.create_table(
        "meter_installations",
        sa.Column("consumer_unit_id", sa.Uuid(), nullable=False),
        sa.Column("meter_id", sa.Uuid(), nullable=False),
        sa.Column("installed_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("installed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("removed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("removed_at IS NULL OR removed_at >= installed_at", name="valid_installation_period"),
        sa.ForeignKeyConstraint(["consumer_unit_id"], ["consumer_units.id"], name=op.f("fk_meter_installations_consumer_unit_id_consumer_units")),
        sa.ForeignKeyConstraint(["installed_by_user_id"], ["users.id"], name=op.f("fk_meter_installations_installed_by_user_id_users")),
        sa.ForeignKeyConstraint(["meter_id"], ["meters.id"], name=op.f("fk_meter_installations_meter_id_meters")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meter_installations")),
    )
    op.create_table(
        "tariff_tiers",
        sa.Column("tariff_plan_id", sa.Uuid(), nullable=False),
        sa.Column("consumption_from", sa.Integer(), nullable=False),
        sa.Column("consumption_to", sa.Integer(), nullable=True),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("fixed_fee", sa.Numeric(12, 2), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("consumption_to IS NULL OR consumption_to >= consumption_from", name="valid_tariff_tier_range"),
        sa.ForeignKeyConstraint(["tariff_plan_id"], ["tariff_plans.id"], name=op.f("fk_tariff_tiers_tariff_plan_id_tariff_plans")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tariff_tiers")),
    )
    op.create_table(
        "invoices",
        sa.Column("consumer_unit_id", sa.Uuid(), nullable=False),
        sa.Column("reading_cycle_id", sa.Uuid(), nullable=True),
        sa.Column("issue_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("paid_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("paid_amount <= total_amount", name="invoice_paid_amount_not_above_total"),
        sa.ForeignKeyConstraint(["consumer_unit_id"], ["consumer_units.id"], name=op.f("fk_invoices_consumer_unit_id_consumer_units")),
        sa.ForeignKeyConstraint(["reading_cycle_id"], ["reading_cycles.id"], name=op.f("fk_invoices_reading_cycle_id_reading_cycles")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invoices")),
        sa.UniqueConstraint("consumer_unit_id", "reading_cycle_id", name="uq_invoice_consumer_unit_cycle"),
    )
    op.create_table(
        "meter_readings",
        sa.Column("consumer_unit_id", sa.Uuid(), nullable=False),
        sa.Column("meter_id", sa.Uuid(), nullable=False),
        sa.Column("reading_cycle_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("previous_reading", sa.Numeric(12, 3), nullable=False),
        sa.Column("current_reading", sa.Numeric(12, 3), nullable=False),
        sa.Column("measured_consumption", sa.Numeric(12, 3), nullable=False),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(length=30), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("current_reading >= previous_reading", name="meter_reading_not_decreasing"),
        sa.ForeignKeyConstraint(["consumer_unit_id"], ["consumer_units.id"], name=op.f("fk_meter_readings_consumer_unit_id_consumer_units")),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], name=op.f("fk_meter_readings_created_by_user_id_users")),
        sa.ForeignKeyConstraint(["meter_id"], ["meters.id"], name=op.f("fk_meter_readings_meter_id_meters")),
        sa.ForeignKeyConstraint(["reading_cycle_id"], ["reading_cycles.id"], name=op.f("fk_meter_readings_reading_cycle_id_reading_cycles")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meter_readings")),
        sa.UniqueConstraint("consumer_unit_id", "reading_cycle_id", name="uq_meter_reading_consumer_unit_cycle"),
    )
    op.create_table(
        "invoice_items",
        sa.Column("invoice_id", sa.Uuid(), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("unit_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], name=op.f("fk_invoice_items_invoice_id_invoices")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invoice_items")),
    )
    op.create_table(
        "payments",
        sa.Column("invoice_id", sa.Uuid(), nullable=False),
        sa.Column("received_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("paid_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=False),
        sa.Column("reference", sa.String(length=100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("paid_amount > 0", name="payment_positive_amount"),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], name=op.f("fk_payments_invoice_id_invoices")),
        sa.ForeignKeyConstraint(["received_by_user_id"], ["users.id"], name=op.f("fk_payments_received_by_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_payments")),
    )


def downgrade() -> None:
    op.drop_table("payments")
    op.drop_table("invoice_items")
    op.drop_table("meter_readings")
    op.drop_table("invoices")
    op.drop_table("tariff_tiers")
    op.drop_table("meter_installations")
    op.drop_table("meter_events")
    op.drop_table("consumer_units")
    op.drop_table("audit_logs")
    op.drop_table("users")
    op.drop_table("tariff_plans")
    op.drop_table("reading_cycles")
    op.drop_table("meters")
    op.drop_table("locations")
    op.drop_table("customers")
