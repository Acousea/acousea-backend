from datetime import datetime

from pydantic import BaseModel, Field


class RockBlockMessage(BaseModel):
    imei: str
    serial: str
    momsn: int
    transmit_time: str
    iridium_latitude: float
    iridium_longitude: float
    iridium_cep: int
    data: str

