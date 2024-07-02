from pydantic import BaseModel

from core.shared.domain.events import DomainEvent


# The response field is the whole response as bytes including header fields
class CommunicationResponseEventPayload(BaseModel):
    opcode: int
    sender_address: int
    recipient_address: int
    response: bytes


class ReceivedCommunicationResponseEvent(DomainEvent[CommunicationResponseEventPayload]):
    name: str = "@communication/received_response"
