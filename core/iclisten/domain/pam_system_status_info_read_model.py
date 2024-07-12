from pydantic import BaseModel


class PAMDeviceStatusReadModel(BaseModel):
    unit_status: int
    battery_status: int
    battery_percentage: float
    temperature: float
    humidity: int



