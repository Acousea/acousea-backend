from fastapi import APIRouter

from apps.rest_api.dependencies import comm_system_request_handler
from core.communication_system.domain.http.change_drifter_op_mode_httprequest import \
    ChangeDrifterOpModeHttpResponse, ChangeDrifterOpModeHttpRequest, ChangeDrifterOpModeParams
from core.communication_system.domain.http.change_localizer_op_mode_httprequest import ChangeLocalizerOpModeHttpRequest, \
    ChangeLocalizerOpModeHttpResponse, ChangeLocalizerOpModeParams
from core.communication_system.domain.http.get_drifter_op_mode_httprequest import GetDrifterOpModeHttpResponse, \
    GetDrifterOpModeHttpRequest
from core.communication_system.domain.http.get_localizer_op_mode_httprequest import GetLocalizerOpModeHttpRequest, \
    GetLocalizerOpModeHttpResponse
from core.communication_system.domain.http.setup_direct_communication_httprequest import \
    SetupDirectCommunicationHttpRequest, SetupDirectCommunicationParams, SetupDirectCommunicationHttpResponse
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.get("/operation-mode/drifter", tags=["op-modes-service"])
def get_drifter_op_mode() -> HttpResponse[GetDrifterOpModeHttpResponse]:
    query = GetDrifterOpModeHttpRequest(request_handler=comm_system_request_handler)
    return query.run()


@router.get("/operation-mode/localizer", tags=["op-modes-service"])
def get_localizer_op_mode() -> HttpResponse[GetLocalizerOpModeHttpResponse]:
    query = GetLocalizerOpModeHttpRequest(request_handler=comm_system_request_handler)
    return query.run()


@router.put("/operation-mode/drifter/{mode}", tags=["op-modes-service"])
def change_drifter_op_mode(mode: str) -> HttpResponse[ChangeDrifterOpModeHttpResponse]:
    query = ChangeDrifterOpModeHttpRequest(request_handler=comm_system_request_handler)
    return query.run(
        ChangeDrifterOpModeParams(
            op_mode=int(mode)
        )
    )


@router.put("/operation-mode/localizer/{mode}", tags=["op-modes-service"])
def change_localizer_op_mode(mode: str, ) -> HttpResponse[ChangeLocalizerOpModeHttpResponse]:
    query = ChangeLocalizerOpModeHttpRequest(request_handler=comm_system_request_handler)
    return query.run(
        ChangeLocalizerOpModeParams(
            op_mode=int(mode)
        )
    )


@router.put("/direct-communication/activate/{serial_number}", tags=["op-modes-service"])
def activate_direct_communication(serial_number: str) -> HttpResponse[SetupDirectCommunicationHttpResponse]:
    query = SetupDirectCommunicationHttpRequest()
    return query.run(
        SetupDirectCommunicationParams(
            serial_number=serial_number
        )
    )


@router.put("/direct-communication/deactivate", tags=["op-modes-service"])
def deactivate_direct_communication(serial_number: str) -> HttpResponse[SetupDirectCommunicationHttpResponse]:
    pass
