from pydantic import BaseModel

from core.communication_system.infrastructure.communicator.communicator_service import CommunicatorService
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDirectCommunicationStatusHttpResponse(BaseModel):
    active: bool


class GetDirectCommunicationStatusHttpRequest(HttpRequest[None, GetDirectCommunicationStatusHttpResponse]):
    def __init__(self, communicator_service: CommunicatorService):
        self.comm_service = communicator_service

    def execute(self, params: None = None) -> HttpResponse[GetDirectCommunicationStatusHttpResponse]:
        print("Get->Selected communicator: ", self.comm_service.selected_communicator.name)
        if self.comm_service.is_serial_communicator_selected():
            return HttpResponse.ok(GetDirectCommunicationStatusHttpResponse(active=True))
        else:
            return HttpResponse.ok(GetDirectCommunicationStatusHttpResponse(active=False))
