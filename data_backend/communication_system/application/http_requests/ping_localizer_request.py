from pydantic import BaseModel

from data_backend.communication_system.application.ports.drifter_request_handler import CommunicationRequestHandler
from data_backend.shared.application.httprequest import HttpRequest
from data_backend.shared.domain.httpresponse import HttpResponse


class PingResponse(BaseModel):
    message: str


class PingLocalizerHttpRequest(HttpRequest[None, PingResponse]):
    def __init__(self, request_handler: CommunicationRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: None = None) -> HttpResponse[PingResponse]:
        response = self.request_handler.ping_localizer()
        if response.empty():
            return HttpResponse.fail(message="No response")
        return HttpResponse.ok(PingResponse(message="Localizer is alive"))
