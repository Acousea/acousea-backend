from pydantic import BaseModel

from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.infrastructure.communication_system_request_handler import \
    CommunicationSystemRequestHandler
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class ChangeDrifterOpModeParams(BaseModel):
    op_mode: int


class ChangeDrifterOpModeHttpResponse(BaseModel):
    op_mode: int


class ChangeDrifterOpModeHttpRequest(HttpRequest[ChangeDrifterOpModeParams, ChangeDrifterOpModeHttpResponse]):
    def __init__(self, request_handler: CommunicationSystemRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: ChangeDrifterOpModeParams | None = None) -> HttpResponse[ChangeDrifterOpModeHttpResponse]:
        if params is None:
            return HttpResponse.fail(message="You need to pass an op_mode")
        if not OperationMode.is_valid_mode(params.op_mode):
            return HttpResponse.fail(message="Invalid op_mode. Must be either 0, 1, 2 or 3")
        response = self.request_handler.change_drifter_op_mode(params.op_mode)
        if response.empty():
            return HttpResponse.fail(message="No response")
        return HttpResponse.ok(ChangeDrifterOpModeHttpResponse(
            op_mode=params.op_mode
        ))
