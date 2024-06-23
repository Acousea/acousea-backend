from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communicator.address import Address
from apps.communication.communicator.operation_codes import OperationCode


class PingRaspberryRequest(CommunicationRequest):
    content = b'\x00\xFF\x00\xFF'

    def __init__(self):
        super().__init__(OperationCode.PING, Address.PI3, self.content)

    def __str__(self):
        return f'PingRaspberryRequest{super().__str__()}'

    def __repr__(self):
        return f'PingRaspberryRequest{super().__repr__()}'
