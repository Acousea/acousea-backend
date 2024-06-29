from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.domain.communicator.requests.change_drifter_opmode_request import \
    ChangeDrifterOpModeRequest
from core.communication_system.domain.communicator.requests.change_localizer_opmode_request import \
    ChangeLocalizerOpModeRequest
from core.communication_system.domain.communicator.requests.ping_drifter_request import PingDrifterRequest
from core.communication_system.domain.communicator.requests.ping_localizer_request import \
    PingLocalizerRequest
from core.communication_system.domain.communicator.requests.ping_raspberry_request import \
    PingRaspberryRequest
from core.communication_system.domain.communicator.responses.ping_drifter_response import \
    PingDrifterResponse
from core.communication_system.domain.communicator.responses.ping_localizer_response import \
    PingLocalizerResponse

from core.communication_system.domain.communicator.responses.ping_raspberry_response import \
    PingRaspberryResponse
from core.shared.application.communicator import Communicator
from core.shared.domain.communicator.communication_response import CommunicationResponse


class CommunicationSystemRequestHandler:
    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def get_drifter_op_mode(self) -> int:
        # TODO: Implement this method with SQLITE database query
        return OperationMode.LAUNCHING_MODE

    def get_localizer_op_mode(self) -> int:
        # TODO: Implement this method with SQLITE database query
        return OperationMode.LAUNCHING_MODE

    def ping_drifter(self) -> CommunicationResponse:
        response_packet: bytes = self.communicator.send_request(PingDrifterRequest())
        response = PingDrifterResponse(response_packet)
        # Check if the response content is the same as the request content
        if response.content() == PingDrifterRequest.content:
            return response
        else:
            raise ValueError("Ping failed")

    def ping_localizer(self) -> CommunicationResponse:
        response_packet = self.communicator.send_request(PingLocalizerRequest())
        response = PingLocalizerResponse(response_packet)
        # Check if the response content is the same as the request content
        if response.content() == PingLocalizerRequest.content:
            return response
        else:
            raise ValueError("Ping failed")

    def ping_raspberry(self) -> CommunicationResponse:
        response_packet = self.communicator.send_request(PingRaspberryRequest())
        response = PingRaspberryResponse(response_packet)
        # Check if the response content is the same as the request content

    def change_drifter_op_mode(self, op_mode: int) -> CommunicationResponse:
        response_packet = self.communicator.send_request(ChangeDrifterOpModeRequest(op_mode))
        response = CommunicationResponse(response_packet)
        # Check if the response content is the same as the request content

    def change_localizer_op_mode(self, op_mode: int) -> CommunicationResponse:
        response_packet = self.communicator.send_request(ChangeLocalizerOpModeRequest(op_mode))
        response = CommunicationResponse(response_packet)
        # Check if the response content is the same as the request content
