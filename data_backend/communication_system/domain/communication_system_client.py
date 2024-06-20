from apps.communication.communication_requests.ping_drifter_request.ping_drifter_request import PingDrifterRequest
from apps.communication.communication_requests.ping_localizer_request.ping_localizer_request import PingLocalizerRequest
from apps.communication.communication_requests.ping_raspberry_request.ping_raspberry_request import PingRaspberryRequest
from apps.communication.communication_responses.communication_response import CommunicationResponse
from apps.communication.communication_responses.ping_drifter_response.ping_drifter_response import PingDrifterResponse
from apps.communication.communication_responses.ping_localizer_response.ping_localizer_response import \
    PingLocalizerResponse
from apps.communication.communication_responses.ping_raspberry_response.ping_raspberry_response import \
    PingRaspberryResponse
from apps.communication.communicator.communicator import Communicator


class CommunicationSystemClient:
    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def ping_drifter(self) -> CommunicationResponse:
        response_packet: bytes = self.communicator.send_request(PingDrifterRequest())
        return PingDrifterResponse(response_packet)

    def ping_localizer(self) -> CommunicationResponse:
        response_packet = self.communicator.send_request(PingLocalizerRequest())
        return PingLocalizerResponse(response_packet)

    def ping_raspberry(self):
        response_packet = self.communicator.send_request(PingRaspberryRequest())
        return PingRaspberryResponse(response_packet)

    def close(self):
        self.communicator.close()

