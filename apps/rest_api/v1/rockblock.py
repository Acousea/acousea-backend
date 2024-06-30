from fastapi import APIRouter, HTTPException, Request

from apps.rest_api.dependencies import rockblock_messages_repository
from core.communication_system.domain.http.rockblock_messages_http_requests import StoreRockBlockMessageHttpRequest, \
    GetRockBlockMessagesHttpRequest, GetRockBlockMessagesParams, StoreRockBlockMessageParams, RockBlockMessageReadModel
from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.post("/webhook/rockblock-packets")
async def receive_rockblock_packet(request: Request):
    try:
        # Leer y imprimir encabezados de la solicitud
        headers = request.headers
        print("Headers:")
        for header, value in headers.items():
            print(f"{header}: {value}")

        # Determinar el tipo de contenido y leer el cuerpo de la solicitud en consecuencia
        if request.headers.get("content-type") == "application/x-www-form-urlencoded":
            form_data = await request.form()
            content = dict(form_data)
        else:
            content = await request.json()

        print("Request Content:")
        print(content)

        # Convertir el contenido a RockBlockMessage
        packet = RockBlockMessage(
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

        query = StoreRockBlockMessageHttpRequest(rockblock_messages_repository)
        response = query.run(StoreRockBlockMessageParams(packet=packet))
        return response
    except Exception as e:
        print("Exception: ", e)
        raise HTTPException(status_code=422, detail=f"Unprocessable Entity: {e}")


@router.get("/webhook/rockblock-packets")
async def get_rockblock_packets() -> HttpResponse[list[RockBlockMessageReadModel]]:
    query = GetRockBlockMessagesHttpRequest(rockblock_messages_repository)
    response = query.run(GetRockBlockMessagesParams())
    return response
