from fastapi import APIRouter, HTTPException, Request, Query, WebSocket, WebSocketDisconnect

from apps.rest_api.dependencies import rockblock_messages_repository, clients, event_bus
from core.communication_system.domain.http.rockblock_messages_http_requests import StoreAndProcessRockBlockMessageHttpRequest, \
    GetAllRockBlockMessagesNonPaginatedHttpRequest, GetAllRockBlockMessagesNonPaginatedParams, StoreRockBlockMessageParams, RockBlockMessageReadModel, \
    GetRockBlockMessagesPaginatedHttpRequest, GetRockBlockMessagesPaginatedParams, PaginatedRockBlockMessagesReadModel
from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.shared.domain.http.httpresponse import HttpResponse
from fastapi import APIRouter, HTTPException, Request, Query, WebSocket, WebSocketDisconnect

from apps.rest_api.dependencies import rockblock_messages_repository, clients
from core.communication_system.domain.http.rockblock_messages_http_requests import StoreAndProcessRockBlockMessageHttpRequest, \
    GetAllRockBlockMessagesNonPaginatedHttpRequest, GetAllRockBlockMessagesNonPaginatedParams, StoreRockBlockMessageParams, RockBlockMessageReadModel, \
    GetRockBlockMessagesPaginatedHttpRequest, GetRockBlockMessagesPaginatedParams, PaginatedRockBlockMessagesReadModel
from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.shared.domain.http.httpresponse import HttpResponse
from core.shared.domain.value_objects import GenericUUID

router = APIRouter()


@router.websocket("/ws/rockblock/messages")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    clients.append(websocket)
    print("New WebSocket accepted, clients: ", len(clients))
    try:
        while True:
            data = await websocket.receive_text()
            # Do something with the data if needed
    except WebSocketDisconnect:
        clients.remove(websocket)


@router.post("/webhook/rockblock-packets")
async def receive_rockblock_packet(request: Request):
    try:
        # content = await debug_request(request) # Debugging
        form_data = await request.form()
        content = dict(form_data)

        # Convertir el contenido a RockBlockMessage
        packet = RockBlockMessage(
            id=GenericUUID.next_id(),
            imei=content.get("imei"),
            serial=content.get("serial"),
            momsn=int(float(content.get("momsn"))),
            transmit_time=content.get("transmit_time"),
            iridium_latitude=float(content.get("iridium_latitude")),
            iridium_longitude=float(content.get("iridium_longitude")),
            iridium_cep=int(float(content.get("iridium_cep"))),
            data=content.get("data")
        )
        print("RockBlockMessage:", packet)
        query = StoreAndProcessRockBlockMessageHttpRequest(rockblock_messages_repository, event_bus)
        response = await query.run(StoreRockBlockMessageParams(message=packet))
        return response
    except Exception as e:
        print("Exception: ", e)
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {e}")


async def debug_request(request):
    # Leer y imprimir encabezados de la solicitud
    headers = request.headers
    print("Headers:")
    for header, value in headers.items():
        print(f"{header}: {value}")
    # Determinar el tipo de contenido y leer el cuerpo de la solicitud en consecuencia
    if request.headers.get("content-type") == "application/x-www-form-urlencoded":
        print("Form Data")
        form_data = await request.form()
        content = dict(form_data)
    else:
        print("JSON Data")
        content = await request.json()
    print("Request Content:")
    print(content)
    return content


@router.get("/rockblock/messages")
async def get_rockblock_packets() -> HttpResponse[list[RockBlockMessageReadModel]]:
    query = GetAllRockBlockMessagesNonPaginatedHttpRequest(rockblock_messages_repository)
    response = query.run(GetAllRockBlockMessagesNonPaginatedParams())
    return response


@router.get("/rockblock/messages/paginated")
async def get_rockblock_packets(
        page: int = Query(1, ge=1),
        rows_per_page: int = Query(10, ge=1, le=50)
) -> HttpResponse[PaginatedRockBlockMessagesReadModel]:
    query = GetRockBlockMessagesPaginatedHttpRequest(rockblock_messages_repository)
    params = GetRockBlockMessagesPaginatedParams(page=page, rows_per_page=rows_per_page)
    response = query.run(params)
    return response
