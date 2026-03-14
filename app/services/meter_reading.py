import uuid

from app.models.meter import MeterReading
from app.repositories.meter_reading import MeterReadingRepository


class MeterReadingService:
    def __init__(self, repository: MeterReadingRepository) -> None:
        self.repository = repository

    def get_existing_reading(self, consumer_unit_id: uuid.UUID, reading_cycle_id: uuid.UUID) -> MeterReading | None:
        return self.repository.get_by_consumer_unit_and_cycle(consumer_unit_id, reading_cycle_id)
