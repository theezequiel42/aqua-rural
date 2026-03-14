import uuid

from app.models.consumer_unit import ConsumerUnit
from app.repositories.base import RepositoryBase


class ConsumerUnitRepository(RepositoryBase):
    def get_by_id(self, consumer_unit_id: uuid.UUID) -> ConsumerUnit | None:
        return self.session.get(ConsumerUnit, consumer_unit_id)
