from fastapi import APIRouter

from apps.rest_api.dependencies import comm_system_request_handler, comm_system_query_repository, communication_request_history_repository, \
    communicator_service
from core.communication_system.domain.http.disable_direct_communication_httprequest import DisableDirectCommunicationHttpRequest, \
    DisableDirectCommunicationHttpResponse
from core.communication_system.domain.http.drifter.change_drifter_op_mode_httprequest import \
    ChangeDrifterOpModeHttpResponse, ChangeDrifterOpModeHttpRequest, ChangeDrifterOpModeParams
from core.communication_system.domain.http.drifter.get_all_drifter_information_httprequest import GetAllCommunicationSystemStatusHttpRequest
from core.communication_system.domain.http.drifter.get_drifter_location_httprequest import GetDrifterLocationHttpRequest, \
    GetDrifterLocationHttpResponse
from core.communication_system.domain.http.drifter.get_drifter_op_mode_httprequest import GetDrifterOpModeHttpResponse, \
    GetDrifterOpModeHttpRequest
from core.communication_system.domain.http.drifter.ping_drifter_request import PingResponse, \
    PingDrifterHttpRequest
from core.communication_system.domain.http.enable_direct_communication_httprequest import \
    EnableDirectCommunicationHttpRequest, EnableDirectCommunicationParams, EnableDirectCommunicationHttpResponse
from core.communication_system.domain.http.flush_communication_request_queue_httprequest import FlushCommunicationRequestQueueHttpRequest, \
    FlushCommunicationRequestQueueHttpResponse
from core.communication_system.domain.http.get_available_com_devices_httprequest import GetAvailableCOMDevicesHttpRequest, \
    AvailableCOMDevicesHttpResponse
from core.communication_system.domain.http.get_direct_communication_status_httprequest import GetDirectCommunicationStatusHttpRequest, \
    GetDirectCommunicationStatusHttpResponse
from core.communication_system.domain.http.localizer.change_localizer_op_mode_httprequest import ChangeLocalizerOpModeHttpRequest, \
    ChangeLocalizerOpModeHttpResponse, ChangeLocalizerOpModeParams
from core.communication_system.domain.http.localizer.get_localizer_location_httprequest import GetLocalizerLocationHttpRequest, \
    GetLocalizerLocationHttpResponse
from core.communication_system.domain.http.localizer.get_localizer_op_mode_httprequest import GetLocalizerOpModeHttpRequest, \
    GetLocalizerOpModeHttpResponse
from core.communication_system.domain.http.localizer.ping_localizer_request import PingLocalizerHttpRequest
from core.communication_system.domain.read_models.communication_system_status_read_model import CommunicationSystemStatusReadModel
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.get("/communication-system/all-status-information", tags=["communication-system-service"])
def get_all_communication_system_status() -> HttpResponse[CommunicationSystemStatusReadModel]:
    query = GetAllCommunicationSystemStatusHttpRequest(repository=comm_system_query_repository)
    return query.run()


@router.get("/communication-system/drifter/operation-mode", tags=["communication-system-service"])
def get_drifter_op_mode() -> HttpResponse[GetDrifterOpModeHttpResponse]:
    query = GetDrifterOpModeHttpRequest(repository=comm_system_query_repository)
    return query.run()


@router.get("/communication-system/localizer/operation-mode", tags=["communication-system-service"])
def get_localizer_op_mode() -> HttpResponse[GetLocalizerOpModeHttpResponse]:
    query = GetLocalizerOpModeHttpRequest(repository=comm_system_query_repository)
    return query.run()


@router.get("/communication-system/drifter/location", tags=["communication-system-service"])
def get_drifter_location() -> HttpResponse[GetDrifterLocationHttpResponse]:
    query = GetDrifterLocationHttpRequest(repository=comm_system_query_repository)
    return query.run()


@router.get("/communication-system/localizer/location", tags=["communication-system-service"])
def get_localizer_location() -> HttpResponse[GetLocalizerLocationHttpResponse]:
    query = GetLocalizerLocationHttpRequest(repository=comm_system_query_repository)
    return query.run()


@router.put("/communication-system/drifter/operation-mode/{mode}", tags=["communication-system-service"])
def change_drifter_op_mode(mode: str) -> HttpResponse[ChangeDrifterOpModeHttpResponse]:
    query = ChangeDrifterOpModeHttpRequest(request_handler=comm_system_request_handler)
    return query.run(
        ChangeDrifterOpModeParams(
            op_mode=int(mode)
        )
    )


@router.put("/communication-system/localizer/operation-mode/{mode}", tags=["communication-system-service"])
def change_localizer_op_mode(mode: str) -> HttpResponse[ChangeLocalizerOpModeHttpResponse]:
    query = ChangeLocalizerOpModeHttpRequest(request_handler=comm_system_request_handler)
    return query.run(
        ChangeLocalizerOpModeParams(
            op_mode=int(mode)
        )
    )


@router.get("/communication-system/direct-communication/status", tags=["communication-system-service"])
def get_direct_communication_status() -> HttpResponse[GetDirectCommunicationStatusHttpResponse]:
    query = GetDirectCommunicationStatusHttpRequest(communicator_service=communicator_service)
    return query.run()


@router.put("/communication-system/direct-communication/activate/{serial_number}", tags=["communication-system-service"])
def activate_direct_communication(serial_number: str) -> HttpResponse[EnableDirectCommunicationHttpResponse]:
    query = EnableDirectCommunicationHttpRequest(communicator_service=communicator_service)
    return query.run(
        EnableDirectCommunicationParams(
            serial_number=serial_number
        )
    )


@router.put("/communication-system/direct-communication/deactivate", tags=["communication-system-service"])
def deactivate_direct_communication() -> HttpResponse[DisableDirectCommunicationHttpResponse]:
    query = DisableDirectCommunicationHttpRequest(communicator_service=communicator_service)
    return query.run()


@router.post("/communication-system/request-queue/flush", tags=["communication-system-service"])
def flush_communication_request_queue() -> HttpResponse[FlushCommunicationRequestQueueHttpResponse]:
    query = FlushCommunicationRequestQueueHttpRequest(comm_system_request_handler, communication_request_history_repository)
    return query.run()


@router.get("/communication-system/available-usb-devices", tags=["communication-system-service"])
def get_available_com_devices() -> HttpResponse[AvailableCOMDevicesHttpResponse]:
    query = GetAvailableCOMDevicesHttpRequest()
    return query.run()


@router.get("/communication-system/drifter/ping", tags=["ping-service"])
def ping_drifter() -> HttpResponse[PingResponse]:
    query = PingDrifterHttpRequest(request_handler=comm_system_request_handler)
    return query.run()


@router.get("/communication-system/localizer/ping", tags=["ping-service"])
def ping_localizer() -> HttpResponse[PingResponse]:
    query = PingLocalizerHttpRequest(request_handler=comm_system_request_handler)
    return query.run()


@router.get("/communication-system/ping/test", tags=["ping-service"])
def ping_test() -> HttpResponse[PingResponse]:
    # Wait for 1 minute
    import time
    time.sleep(30)
    return HttpResponse.ok(PingResponse(message="Test is alive"))
