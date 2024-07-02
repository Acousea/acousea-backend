from pydantic import BaseModel

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDrifterOpModeHttpResponse(BaseModel):
    mode: int


class GetDrifterOpModeHttpRequest(HttpRequest[None, GetDrifterOpModeHttpResponse]):
    def __init__(self, repository: CommunicationSystemQueryRepository):
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[GetDrifterOpModeHttpResponse]:
        response = self.repository.get_drifter_op_mode()
        if response is None:
            return HttpResponse.fail(message="Drifter op mode not found (unknown)")
        return HttpResponse.ok(GetDrifterOpModeHttpResponse(mode=response))
