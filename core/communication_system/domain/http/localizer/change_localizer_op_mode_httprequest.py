from pydantic import BaseModel

from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.domain.communicator.communication_result import CommunicationStatus
from core.communication_system.infrastructure.communication_system_client import \
    CommunicationSystemClient
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class ChangeLocalizerOpModeParams(BaseModel):
    op_mode: int


class ChangeLocalizerOpModeHttpResponse(BaseModel):
    op_mode: int


class ChangeLocalizerOpModeHttpRequest(HttpRequest[ChangeLocalizerOpModeParams, ChangeLocalizerOpModeHttpResponse]):
    def __init__(self, request_handler: CommunicationSystemClient):
        self.request_handler = request_handler

    def execute(self, params: ChangeLocalizerOpModeParams | None = None) -> HttpResponse[ChangeLocalizerOpModeHttpResponse]:
        if params is None:
            return HttpResponse.fail(message="You need to pass an op_mode")
        if not OperationMode.is_valid_mode(params.op_mode):
            return HttpResponse.fail(message="Invalid op_mode. Must be either 0, 1, 2 or 3")
        response = self.request_handler.change_localizer_op_mode(params.op_mode)
        if response.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                ChangeLocalizerOpModeHttpResponse(
                    op_mode=params.op_mode,
                ))
        return HttpResponse.fail(message=response.message, code=response.error_code)
