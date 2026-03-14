from app.schemas.base import SchemaBase, TimestampedReadSchema


class CustomerCreate(SchemaBase):
    full_name: str
    document_number: str | None = None
    email: str | None = None
    phone_number: str | None = None
    is_active: bool = True


class CustomerRead(TimestampedReadSchema, CustomerCreate):
    pass
