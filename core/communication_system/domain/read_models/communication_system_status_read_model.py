from pydantic import BaseModel

from core.shared.domain.read_models.storage_read_model import StorageReadModel


class CommunicationSystemStatusReadModel(BaseModel):
    epoch_time: str
    latitude: float
    longitude: float
    battery_percentage: int
    battery_status: int
    temperature: float
    operation_mode: int
    storage: StorageReadModel


