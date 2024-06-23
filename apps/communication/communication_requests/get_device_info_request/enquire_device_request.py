from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communicator.address import Address
from apps.communication.communicator.operation_codes import OperationCode


class GetDeviceInfoRequest(CommunicationRequest):
    def __init__(self):
        super().__init__(OperationCode.GET_DEVICE_INFO, Address.PI3, b'')

    def __str__(self):
        return f'GetDeviceInfoRequest{super().__str__()}'

    def __repr__(self):
        return f'GetDeviceInfoRequest{super().__repr__()}'

