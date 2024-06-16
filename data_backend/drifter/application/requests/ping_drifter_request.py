from pydantic import BaseModel

from data_backend.drifter.application.ports.drifter_request_handler import DrifterRequestHandler
from data_backend.iclisten.application.ports.iclisten_request_handler import ICListenRequestHandler

from data_backend.shared.application.httprequest import HttpRequest
from data_backend.shared.domain.httpresponse import HttpResponse


class PingResponse(BaseModel):
    message: str


class PingRequest(HttpRequest[None, PingResponse]):
    def __init__(self, request_handler: DrifterRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: None = None) -> HttpResponse[PingResponse]:
        response = self.request_handler.ping()
        if response.empty():
            return HttpResponse.fail(message="No response")
        return HttpResponse.ok(PingResponse(message="Drifter is alive"))
