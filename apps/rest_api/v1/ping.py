from fastapi import APIRouter

from apps.rest_api.dependencies import comm_system_request_handler
from core.communication_system.domain.http.ping_drifter_request import PingResponse, \
    PingDrifterHttpRequest
from core.communication_system.domain.http.ping_localizer_request import PingLocalizerHttpRequest
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.get("/ping/communication_system", tags=["ping-service"])
def ping_drifter() -> HttpResponse[PingResponse]:
    query = PingDrifterHttpRequest(request_handler=comm_system_request_handler)
    return query.run()


@router.get("/ping/localizer", tags=["ping-service"])
def ping_localizer() -> HttpResponse[PingResponse]:
    query = PingLocalizerHttpRequest(request_handler=comm_system_request_handler)
    return query.run()


@router.get("/ping/test", tags=["ping-service"])
def ping_test() -> HttpResponse[PingResponse]:
    # Wait for 1 minute
    import time
    time.sleep(30)
    return HttpResponse.ok(PingResponse(message="Test is alive"))


