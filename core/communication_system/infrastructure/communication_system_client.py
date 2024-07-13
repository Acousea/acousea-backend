from core.communication_system.domain.communicator.communication_result import CommunicationResult
from core.communication_system.domain.communicator.requests.change_drifter_opmode_request import \
    ChangeDrifterOpModeRequest
from core.communication_system.domain.communicator.requests.change_localizer_opmode_request import \
    ChangeLocalizerOpModeRequest
from core.communication_system.domain.communicator.requests.get_drifter_reporting_periods_request import GetDrifterReportingPeriodsRequest
from core.communication_system.domain.communicator.requests.ping_drifter_request import PingDrifterRequest
from core.communication_system.domain.communicator.requests.ping_localizer_request import \
    PingLocalizerRequest
from core.communication_system.domain.communicator.requests.ping_raspberry_request import \
    PingRaspberryRequest
from core.communication_system.domain.communicator.requests.set_drifter_reporting_periods_request import SetDrifterReportingPeriodsRequest
from core.communication_system.domain.reporting_periods import ReportingPeriods
from core.communication_system.infrastructure.communicator.communicator_service import CommunicatorService


class CommunicationSystemClient:
    def __init__(self, communicator_service: CommunicatorService):
        self.communicator_service = communicator_service

    def ping_drifter(self) -> CommunicationResult:
        result = self.communicator_service.send_request(PingDrifterRequest())
        return result

    def ping_localizer(self) -> CommunicationResult:
        result = self.communicator_service.send_request(PingLocalizerRequest())
        return result

    def ping_raspberry(self) -> CommunicationResult:
        result = self.communicator_service.send_request(PingRaspberryRequest())
        return result

    def change_drifter_op_mode(self, op_mode: int) -> CommunicationResult:
        result = self.communicator_service.send_request(ChangeDrifterOpModeRequest(op_mode))
        return result

    def change_localizer_op_mode(self, op_mode: int) -> CommunicationResult:
        result = self.communicator_service.send_request(ChangeLocalizerOpModeRequest(op_mode))
        return result

    def flush_communication_request_queue(self) -> CommunicationResult:
        result = self.communicator_service.flush_communication_request_queue(localizer=True, drifter=True)
        return result

    def set_drifter_reporting_periods(self, params: ReportingPeriods) -> CommunicationResult:
        result = self.communicator_service.send_request(SetDrifterReportingPeriodsRequest(params))
        return result

    def get_updated_drifter_reporting_periods(self):
        result = self.communicator_service.send_request(GetDrifterReportingPeriodsRequest())
        return result

