from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communicator.address import Address


class PingLocalizerRequest(CommunicationRequest):
    content = b'\x00\xFF\x00\xFF'

    def __init__(self):
        super().__init__('0', Address.LOCALIZER, self.content)

    def __str__(self):
        return f'PingLocalizerRequest{super().__str__()}'

    def __repr__(self):
        return f'PingLocalizerRequest{super().__repr__()}'

