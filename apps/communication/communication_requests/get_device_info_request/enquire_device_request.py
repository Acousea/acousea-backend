from apps.communication.communication_requests.communication_request import CommunicationRequest


class GetDeviceInfoRequest(CommunicationRequest):
    def __init__(self):
        super().__init__('E', b'')

    def __str__(self):
        return f'EnquireDeviceRequest: {self.code} {self.payload}\n'
