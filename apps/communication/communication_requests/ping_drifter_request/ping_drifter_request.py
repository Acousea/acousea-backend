from apps.communication.communication_requests.communication_request import CommunicationRequest


class PingDrifterRequest(CommunicationRequest):
    def __init__(self):
        super().__init__('0', b'\x00\xFF\x00\xFF')

    def __str__(self):
        return f'PingDrifterRequest: {self.code} {self.payload}\n'
