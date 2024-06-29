from pydantic import BaseModel

from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.infrastructure.communication_system_request_handler import \
    CommunicationSystemRequestHandler
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDrifterOpModeHttpResponse(BaseModel):
    mode: int


class GetDrifterOpModeHttpRequest(HttpRequest[None, GetDrifterOpModeHttpResponse]):
    def __init__(self, request_handler: CommunicationSystemRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: None = None) -> HttpResponse[GetDrifterOpModeHttpResponse]:
        response = self.request_handler.get_drifter_op_mode()
        if response is None:
            return HttpResponse.fail(message="Drifter op mode not found (unknown)")
        return HttpResponse.ok(GetDrifterOpModeHttpResponse(mode=response))
