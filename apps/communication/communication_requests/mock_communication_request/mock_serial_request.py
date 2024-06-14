from apps.communication.communication_requests.communication_request import CommunicationRequest


class MockCommunicationRequest(CommunicationRequest):
    def __init__(self):
        super().__init__('0', b'\x00\x01\x00\x01')

    def __str__(self):
        return f'MockCommunicationRequest: {self.code} {self.payload}\n'
