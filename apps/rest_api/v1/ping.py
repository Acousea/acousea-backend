from fastapi import APIRouter

from apps.rest_api.dependencies import drifter_query_handler
from data_backend.drifter.application.requests.ping_drifter_request import PingRequest, PingResponse
from data_backend.shared.domain.httpresponse import HttpResponse

router = APIRouter()


@router.get("/ping", tags=["ping-service"])
def ping_drifter() -> HttpResponse[PingResponse]:
    query = PingRequest(request_handler=drifter_query_handler)
    return query.run()
