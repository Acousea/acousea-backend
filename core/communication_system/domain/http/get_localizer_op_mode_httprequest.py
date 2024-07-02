from pydantic import BaseModel

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.infrastructure.communication_system_client import \
    CommunicationSystemClient
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetLocalizerOpModeHttpResponse(BaseModel):
    mode: int


class GetLocalizerOpModeHttpRequest(HttpRequest[None, GetLocalizerOpModeHttpResponse]):
    def __init__(self, repository: CommunicationSystemQueryRepository):
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[GetLocalizerOpModeHttpResponse]:
        response = self.repository.get_localizer_op_mode()
        if response is None:
            return HttpResponse.fail(message="Localizer op mode not found (unknown)")
        return HttpResponse.ok(GetLocalizerOpModeHttpResponse(mode=response))
