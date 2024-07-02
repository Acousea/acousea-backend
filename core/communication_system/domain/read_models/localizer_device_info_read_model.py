from pydantic import BaseModel


class LocalizerDeviceInfoReadModel(BaseModel):
    epoch_time: str
    battery_percent: int
    latitude: float
    longitude: float
    operation_mode: int

