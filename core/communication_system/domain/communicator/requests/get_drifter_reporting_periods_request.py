from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class GetDrifterReportingPeriodsRequest(CommunicationRequest):
    def __init__(self):
        super().__init__(OperationCode.GET_REPORTING_PERIODS, Address.DRIFTER, b'')

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
