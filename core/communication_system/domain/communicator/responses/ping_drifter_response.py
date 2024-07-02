from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class PingDrifterResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)

    def __str__(self):
        return f'PingDrifterResponse{super().__str__()}'

    def __repr__(self):
        return f'PingDrifterResponse{super().__repr__()}'
