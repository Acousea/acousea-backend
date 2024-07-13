from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.reporting_periods import ReportingPeriods
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class RetrieveDrifterReportingPeriodsHttpRequest(HttpRequest[None, ReportingPeriods]):
    def __init__(self, repository: CommunicationSystemQueryRepository):
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[ReportingPeriods]:
        reporting_periods: ReportingPeriods | None = self.repository.get_drifter_reporting_periods()
        if reporting_periods is not None:
            return HttpResponse.ok(
                reporting_periods
            )
        return HttpResponse.fail(message="No reporting periods found")
