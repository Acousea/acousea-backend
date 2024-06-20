from apps.communication.communication_requests.get_device_info_request.enquire_device_request import \
    GetDeviceInfoRequest
from apps.communication.communication_requests.mock_communication_request.mock_communication_request import \
    MockCommunicationRequest
from apps.communication.communication_responses.get_device_info_response.get_device_info_response import \
    GetDeviceInfoResponse
from apps.communication.communication_responses.mock_communication_response.mock_communication_response import \
    MockCommunicationResponse
from apps.communication.communicator.communicator import Communicator


class ICListenClient:
    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def get_device_info(self) -> GetDeviceInfoResponse:
        response_packet = self.communicator.send_request(GetDeviceInfoRequest())
        return GetDeviceInfoResponse(response_packet)  # Convertimos la respuesta genérica a específica

    def mock_request(self) -> MockCommunicationResponse:
        response_packet = self.communicator.send_request(MockCommunicationRequest())
        return MockCommunicationResponse(response_packet)

    def close(self):
        self.communicator.close()
