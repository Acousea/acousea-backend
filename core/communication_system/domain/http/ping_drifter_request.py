from pydantic import BaseModel

from core.communication_system.infrastructure.communication_system_request_handler import \
    CommunicationSystemRequestHandler
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class PingResponse(BaseModel):
    message: str


class PingDrifterHttpRequest(HttpRequest[None, PingResponse]):
    def __init__(self, request_handler: CommunicationSystemRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: None = None) -> HttpResponse[PingResponse]:
        response = self.request_handler.ping_drifter()
        if response.empty():
            return HttpResponse.fail(message="No response")
        return HttpResponse.ok(PingResponse(message="Drifter is alive"))
