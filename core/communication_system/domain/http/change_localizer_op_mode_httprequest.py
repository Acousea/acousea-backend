from pydantic import BaseModel

from core.communication_system.infrastructure.communication_system_request_handler import \
    CommunicationSystemRequestHandler
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class ChangeLocalizerOpModeParams(BaseModel):
    op_mode: int


class ChangeLocalizerOpModeHttpResponse(BaseModel):
    message: str


class ChangeLocalizerOpModeHttpRequest(HttpRequest[ChangeLocalizerOpModeParams, ChangeLocalizerOpModeHttpResponse]):
    def __init__(self, request_handler: CommunicationSystemRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: ChangeLocalizerOpModeParams | None = None) -> HttpResponse[ChangeLocalizerOpModeHttpResponse]:
        if params is None:
            return HttpResponse.fail(message="You need to pass an op_mode")
        if params.op_mode not in [0, 1, 2, 3]:
            return HttpResponse.fail(message="Invalid op_mode. Must be either 0, 1, 2 or 3")

        response = self.request_handler.change_localizer_op_mode(params.op_mode)
        if response.empty():
            return HttpResponse.fail(message="No response")
        return HttpResponse.ok(
            ChangeLocalizerOpModeHttpResponse(message="Localizer mode set to " + str(params.op_mode)))
