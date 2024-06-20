from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communicator.address import Address


class GetDeviceInfoRequest(CommunicationRequest):
    def __init__(self):
        super().__init__('E', Address.PI3, b'')

    def __str__(self):
        return f'GetDeviceInfoRequest{super().__str__()}'

    def __repr__(self):
        return f'GetDeviceInfoRequest{super().__repr__()}'

