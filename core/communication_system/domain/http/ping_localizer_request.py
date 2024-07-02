from pydantic import BaseModel

from core.communication_system.infrastructure.communication_system_client import \
    CommunicationSystemClient
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class PingResponse(BaseModel):
    message: str


class PingLocalizerHttpRequest(HttpRequest[None, PingResponse]):
    def __init__(self, request_handler: CommunicationSystemClient):
        self.request_handler = request_handler

    def execute(self, params: None = None) -> HttpResponse[PingResponse]:
        response = self.request_handler.ping_localizer()
        if response.empty():
            return HttpResponse.fail(message="No response")
        return HttpResponse.ok(PingResponse(message="Localizer is alive"))
