from pydantic import BaseModel

from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.domain.communicator.communication_result import CommunicationStatus, CommunicationResultHttpResponse
from core.communication_system.infrastructure.communication_system_client import \
    CommunicationSystemClient
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDrifterReportingPeriodsHttpRequest(HttpRequest[None, CommunicationResultHttpResponse]):
    def __init__(self, request_handler: CommunicationSystemClient):
        self.request_handler = request_handler

    def execute(self, params: None = None) -> HttpResponse[CommunicationResultHttpResponse]:
        result = self.request_handler.get_updated_drifter_reporting_periods()
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                CommunicationResultHttpResponse(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)
