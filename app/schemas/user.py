from app.schemas.base import SchemaBase, TimestampedReadSchema


class UserCreate(SchemaBase):
    full_name: str
    email: str
    is_active: bool = True


class UserRead(TimestampedReadSchema, UserCreate):
    pass
