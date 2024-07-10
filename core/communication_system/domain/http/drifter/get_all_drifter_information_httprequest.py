from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.read_models.communication_system_status_read_model import CommunicationSystemStatusReadModel
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetAllCommunicationSystemStatusHttpRequest(HttpRequest[None, CommunicationSystemStatusReadModel]):
    def __init__(self, repository: CommunicationSystemQueryRepository):
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[CommunicationSystemStatusReadModel]:
        response: CommunicationSystemStatusReadModel = self.repository.get_communication_system_status()
        if response is None:
            return HttpResponse.fail(message="Communication system information not found (unknown)")
        return HttpResponse.ok(
            response
        )
