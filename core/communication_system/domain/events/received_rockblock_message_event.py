from pydantic import BaseModel

from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.shared.domain.events import DomainEvent


class ReceivedRockBlockMessagePayload(BaseModel):
    message: RockBlockMessage


class ReceivedRockBlockMessageEvent(DomainEvent[ReceivedRockBlockMessagePayload]):
    name: str = "@rockblock/received_message"
