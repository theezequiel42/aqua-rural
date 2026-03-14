import uuid

from sqlalchemy import select

from app.models.meter import MeterReading
from app.repositories.base import RepositoryBase


class MeterReadingRepository(RepositoryBase):
    def get_by_consumer_unit_and_cycle(self, consumer_unit_id: uuid.UUID, reading_cycle_id: uuid.UUID) -> MeterReading | None:
        statement = select(MeterReading).where(
            MeterReading.consumer_unit_id == consumer_unit_id,
            MeterReading.reading_cycle_id == reading_cycle_id,
        )
        return self.session.execute(statement).scalar_one_or_none()
