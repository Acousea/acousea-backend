# queries.py
from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.communication_system.infrastructure.rockblock_messages_repository import RockBlockMessagesRepository
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


# Params and Responses
class StoreRockBlockMessageParams(BaseModel):
    packet: RockBlockMessage


class GetRockBlockMessagesParams(BaseModel):
    pass


class RockBlockMessageReadModel(BaseModel):
    imei: str
    serial: str
    momsn: int
    transmit_time: str
    iridium_latitude: float
    iridium_longitude: float
    iridium_cep: int
    data: str


# Request Handlers
class StoreRockBlockMessageHttpRequest(HttpRequest[StoreRockBlockMessageParams, RockBlockMessageReadModel]):
    def __init__(self, rockblock_messages_repository: RockBlockMessagesRepository):
        self.rockblock_messages_repository = rockblock_messages_repository

    def execute(self, params: StoreRockBlockMessageParams | None = None) -> HttpResponse[RockBlockMessageReadModel]:
        if params is None:
            return HttpResponse.fail(message="You need to specify a packet")
        stored_message = self.rockblock_messages_repository.store_message(params.packet)
        # If successful here must trigger an event to process the last received message
        return HttpResponse.ok(RockBlockMessageReadModel(**stored_message.model_dump()))


class GetRockBlockMessagesHttpRequest(HttpRequest[GetRockBlockMessagesParams, list[RockBlockMessageReadModel]]):
    def __init__(self, rockblock_messages_repository: RockBlockMessagesRepository):
        self.rockblock_messages_repository = rockblock_messages_repository

    def execute(self, params: GetRockBlockMessagesParams | None = None) -> HttpResponse[
        List[RockBlockMessageReadModel]]:
        messages = self.rockblock_messages_repository.get_messages()
        return HttpResponse.ok([RockBlockMessageReadModel(**message.model_dump()) for message in messages])
