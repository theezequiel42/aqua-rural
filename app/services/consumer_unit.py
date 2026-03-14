import uuid

from app.models.consumer_unit import ConsumerUnit
from app.repositories.consumer_unit import ConsumerUnitRepository


class ConsumerUnitService:
    def __init__(self, repository: ConsumerUnitRepository) -> None:
        self.repository = repository

    def get_consumer_unit(self, consumer_unit_id: uuid.UUID) -> ConsumerUnit | None:
        return self.repository.get_by_id(consumer_unit_id)
