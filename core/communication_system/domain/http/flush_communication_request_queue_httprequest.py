from pydantic import BaseModel

from core.communication_system.application.ports.communication_request_history_repository import CommunicationRequestHistoryRepository
from core.communication_system.domain.communicator.communication_result import CommunicationStatus
from core.communication_system.infrastructure.communication_system_client import \
    CommunicationSystemClient
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class FlushCommunicationRequestQueueHttpResponse(BaseModel):
    status: str
    message: str


class FlushCommunicationRequestQueueHttpRequest(HttpRequest[None, FlushCommunicationRequestQueueHttpResponse]):
    def __init__(self, comm_system_client: CommunicationSystemClient, repository: CommunicationRequestHistoryRepository):
        self.comm_system_client = comm_system_client
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[FlushCommunicationRequestQueueHttpResponse]:
        result = self.comm_system_client.flush_communication_request_queue()
        self.repository.flush_all_unresolved_requests()
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                FlushCommunicationRequestQueueHttpResponse(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)
