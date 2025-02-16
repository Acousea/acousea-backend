from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class PingDrifterRequest(CommunicationRequest):
    # Campo estático para el payload de la solicitud
    content: bytes = b'\x00\xFF\x00\xFF'

    def __init__(self):
        # Static field containing the payload of the request
        super().__init__(OperationCode.PING, Address.DRIFTER, self.content)

    def __str__(self):
        return f'PingDrifterRequest{super().__str__()}'

    def __repr__(self):
        return f'PingDrifterRequest{super().__repr__()}'

