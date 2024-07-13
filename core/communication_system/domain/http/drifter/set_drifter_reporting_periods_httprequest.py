from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.domain.communicator.communication_result import CommunicationStatus, CommunicationResultHttpResponse
from core.communication_system.domain.reporting_periods import ReportingPeriods
from core.communication_system.infrastructure.communication_system_client import \
    CommunicationSystemClient
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class SetDrifterReportingPeriodsHttpRequest(HttpRequest[ReportingPeriods, CommunicationResultHttpResponse]):
    def __init__(self, request_handler: CommunicationSystemClient):
        self.request_handler = request_handler

    def execute(self, params: ReportingPeriods | None = None) -> HttpResponse[CommunicationResultHttpResponse]:
        if params is None:
            return HttpResponse.fail(message="You need to pass reporting periods")
        result = self.request_handler.set_drifter_reporting_periods(params)
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                CommunicationResultHttpResponse(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)
