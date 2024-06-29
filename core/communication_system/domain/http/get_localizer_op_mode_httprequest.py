from pydantic import BaseModel

from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.infrastructure.communication_system_request_handler import \
    CommunicationSystemRequestHandler
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetLocalizerOpModeHttpResponse(BaseModel):
    mode: int


class GetLocalizerOpModeHttpRequest(HttpRequest[None, GetLocalizerOpModeHttpResponse]):
    def __init__(self, request_handler: CommunicationSystemRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: None = None) -> HttpResponse[GetLocalizerOpModeHttpResponse]:
        response = self.request_handler.get_localizer_op_mode()
        if response is None:
            return HttpResponse.fail(message="Localizer op mode not found (unknown)")
        return HttpResponse.ok(GetLocalizerOpModeHttpResponse(mode=response))
