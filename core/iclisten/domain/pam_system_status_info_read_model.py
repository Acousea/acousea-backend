from pydantic import BaseModel

from core.shared.domain.read_models.storage_read_model import StorageReadModel


class PAMDeviceStatusReadModel(BaseModel):
    unit_status: int
    battery_status: int
    battery_percentage: float
    temperature: float
    humidity: int
    storage: StorageReadModel



