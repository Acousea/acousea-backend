from core.shared.domain.entity import AggregateRoot
from core.shared.domain.value_objects import GenericUUID


class RockBlockMessage(AggregateRoot[GenericUUID]):
    imei: str
    serial: str
    momsn: int
    transmit_time: str
    iridium_latitude: float
    iridium_longitude: float
    iridium_cep: int
    data: str
