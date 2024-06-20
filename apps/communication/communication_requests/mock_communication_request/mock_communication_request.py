from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communicator.address import Address


class MockCommunicationRequest(CommunicationRequest):
    def __init__(self):
        super().__init__('0', Address.BACKEND, b'\x00\x01\x00\x01')

    def __str__(self):
        return f'MockCommunicationRequest{super().__str__()}'

    def __repr__(self):
        return f'MockCommunicationRequest{super().__repr__()}'

