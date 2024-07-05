# queries.py
import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from core.communication_system.application.handlers.received_rockblock_message_handler import ReceivedRockBlockMessagePayload
from core.communication_system.domain.communicator.communication_response import CommunicationResponse
from core.communication_system.domain.events.received_communication_response_event import ReceivedCommunicationResponseEvent, \
    CommunicationResponseEventPayload
from core.communication_system.domain.events.received_rockblock_message_event import ReceivedRockBlockMessageEvent
from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.communication_system.infrastructure.rockblock_messages_repository import RockBlockMessagesRepository
from core.shared.application.event_bus import EventBus
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse

load_dotenv()
localizer_imei = os.getenv('LOCALIZER_IMEI')
drifter_imei = os.getenv('DRIFTER_IMEI')


# Params and Responses
class StoreRockBlockMessageParams(BaseModel):
    message: RockBlockMessage


class GetAllRockBlockMessagesNonPaginatedParams(BaseModel):
    pass


class GetRockBlockMessagesPaginatedParams(BaseModel):
    page: int
    rows_per_page: int


class RockBlockMessageReadModel(BaseModel):
    imei: str
    serial: str
    momsn: int
    transmit_time: str
    iridium_latitude: float
    iridium_longitude: float
    iridium_cep: int
    data: str
    device: str = Field(default="unknown")

    def __init__(self, **data):
        super().__init__(**data)
        self.device = self._set_device_based_on_imei(self.imei)

    @staticmethod
    def _set_device_based_on_imei(imei: str) -> str:
        if imei == str(drifter_imei):
            return 'drifter'
        elif imei == str(localizer_imei):
            return 'localizer'
        return 'unknown'


class PaginatedRockBlockMessagesReadModel(BaseModel):
    data: List[RockBlockMessageReadModel]
    total: int


# Request Handlers
class StoreAndProcessRockBlockMessageHttpRequest(HttpRequest[StoreRockBlockMessageParams, RockBlockMessageReadModel]):
    def __init__(self, rockblock_messages_repository: RockBlockMessagesRepository, event_bus: EventBus):
        self.rockblock_messages_repository = rockblock_messages_repository
        self.event_bus = event_bus

    async def execute(self, params: StoreRockBlockMessageParams | None = None) -> HttpResponse[RockBlockMessageReadModel]:
        if params is None:
            return HttpResponse.fail(message="You need to specify a packet")
        stored_message: RockBlockMessage = self.rockblock_messages_repository.store_message(params.message)
        stored_message.register_event(
            ReceivedRockBlockMessageEvent(
                payload=ReceivedRockBlockMessagePayload(
                    message=params.message)
            )
        )
        # Only trigger the event if there is data > 0 and it is not a test message
        if len(params.message.data) > 0 and params.message.data != "4162636465666768696a6b6c6d6e6f707172737475767778797a31323334353637383930":
            communication_response = CommunicationResponse(bytes.fromhex(params.message.data))
            stored_message.register_event(
                ReceivedCommunicationResponseEvent(
                    payload=CommunicationResponseEventPayload(
                        opcode=communication_response.opcode,
                        sender_address=communication_response.sender_address,
                        recipient_address=communication_response.recipient_address,
                        response=communication_response.response
                    )
                )
            )
            await self.event_bus.notify_all(stored_message.collect_events())
        # If successful here must trigger an event to process the last received message
        return HttpResponse.ok(RockBlockMessageReadModel(**stored_message.model_dump()))


class GetAllRockBlockMessagesNonPaginatedHttpRequest(HttpRequest[GetAllRockBlockMessagesNonPaginatedParams, list[RockBlockMessageReadModel]]):
    def __init__(self, rockblock_messages_repository: RockBlockMessagesRepository):
        self.rockblock_messages_repository = rockblock_messages_repository

    def execute(self, params: GetAllRockBlockMessagesNonPaginatedParams | None = None) -> HttpResponse[
        List[RockBlockMessageReadModel]]:
        messages = self.rockblock_messages_repository.get_all_messages_non_paginated()
        return HttpResponse.ok([RockBlockMessageReadModel(**message.model_dump()) for message in messages])


class GetRockBlockMessagesPaginatedHttpRequest(HttpRequest[GetRockBlockMessagesPaginatedParams, PaginatedRockBlockMessagesReadModel]):
    def __init__(self, rockblock_messages_repository: RockBlockMessagesRepository):
        self.rockblock_messages_repository = rockblock_messages_repository

    def execute(self, params: GetRockBlockMessagesPaginatedParams | None = None) -> HttpResponse[PaginatedRockBlockMessagesReadModel]:
        if params is None:
            return HttpResponse.fail(message="You need to specify pagination parameters")
        messages, total = self.rockblock_messages_repository.get_messages_paginated_sorted_by_date(params.page, params.rows_per_page)
        return HttpResponse.ok(PaginatedRockBlockMessagesReadModel(
            data=[RockBlockMessageReadModel(**message.model_dump()) for message in messages],
            total=total
        ))
