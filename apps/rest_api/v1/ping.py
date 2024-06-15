from fastapi import APIRouter

from apps.rest_api.dependencies import selected_communicator
from data_backend.drifter.application.requests.ping_drifter_request import PingDrifterRequest, PingDrifterResponse
from data_backend.shared.domain.httpresponse import HttpResponse

router = APIRouter()


@router.get("/ping", tags=["ping-service"])
def ping_drifter() -> HttpResponse[PingDrifterResponse]:
    query = PingDrifterRequest(communicator=selected_communicator)
    return query.run()
