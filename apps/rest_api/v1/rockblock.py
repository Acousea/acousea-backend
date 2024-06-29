from fastapi import APIRouter

from apps.rest_api.dependencies import rockblock_messages_repository
from core.communication_system.domain.http.rockblock_messages_http_requests import StoreRockBlockMessageHttpRequest, \
    GetRockBlockMessagesHttpRequest, GetRockBlockMessagesParams, StoreRockBlockMessageParams, RockBlockMessageReadModel
from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.post("/webhook/rockblock-packets")
async def receive_rockblock_packet(packet: RockBlockMessage):
    query = StoreRockBlockMessageHttpRequest(rockblock_messages_repository)
    response = query.run(StoreRockBlockMessageParams(packet=packet))
    return response


@router.get("/webhook/rockblock-packets")
async def get_rockblock_packets() -> HttpResponse[list[RockBlockMessageReadModel]]:
    query = GetRockBlockMessagesHttpRequest(rockblock_messages_repository)
    response = query.run(GetRockBlockMessagesParams())
    return response
