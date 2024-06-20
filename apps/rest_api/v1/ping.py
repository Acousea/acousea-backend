from fastapi import APIRouter

from apps.rest_api.dependencies import drifter_query_handler
from data_backend.communication_system.application.http_requests.ping_drifter_request import PingResponse, \
    PingDrifterHttpRequest
from data_backend.communication_system.application.http_requests.ping_localizer_request import PingLocalizerHttpRequest

from data_backend.shared.domain.httpresponse import HttpResponse

router = APIRouter()


@router.get("/ping/communication_system", tags=["ping-service"])
def ping_drifter() -> HttpResponse[PingResponse]:
    query = PingDrifterHttpRequest(request_handler=drifter_query_handler)
    return query.run()


@router.get("/ping/localizer", tags=["ping-service"])
def ping_localizer() -> HttpResponse[PingResponse]:
    query = PingLocalizerHttpRequest(request_handler=drifter_query_handler)
    return query.run()


@router.get("/ping/test", tags=["ping-service"])
def ping_test() -> HttpResponse[PingResponse]:
    # Wait for 1 minute
    import time
    time.sleep(30)
    return HttpResponse.ok(PingResponse(message="Test is alive"))
