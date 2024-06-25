from core.shared.domain.communicator.communication_request import CommunicationRequest
from core.shared.domain.address import Address

from core.shared.domain.operation_codes import OperationCode


class GetDeviceInfoRequest(CommunicationRequest):
    def __init__(self):
        super().__init__(OperationCode.GET_DEVICE_INFO, Address.PI3, b'')

    def __str__(self):
        return f'GetDeviceInfoRequest{super().__str__()}'

    def __repr__(self):
        return f'GetDeviceInfoRequest{super().__repr__()}'

