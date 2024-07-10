from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.shared.domain.address import Address

from core.shared.domain.operation_codes import OperationCode


class GetDeviceLoggingConfigRequest(CommunicationRequest):
    def __init__(self):
        super().__init__(OperationCode.GET_PAM_DEVICE_LOGGING_CONFIG, Address.PI3, b'')

    def __str__(self):
        return f'GetDeviceLoggingConfigRequest{super().__str__()}'

    def __repr__(self):
        return f'GetDeviceLoggingConfigRequest{super().__repr__()}'
