from core.shared.domain.communicator.communication_request import CommunicationRequest
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class PingRaspberryRequest(CommunicationRequest):
    content = b'\x00\xFF\x00\xFF'

    def __init__(self):
        super().__init__(OperationCode.PING, Address.PI3, self.content)

    def __str__(self):
        return f'PingRaspberryRequest{super().__str__()}'

    def __repr__(self):
        return f'PingRaspberryRequest{super().__repr__()}'
