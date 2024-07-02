from core.communication_system.application.ports.communicator import Communicator
from core.communication_system.domain.communicator.communication_result import CommunicationResult
from core.communication_system.domain.communicator.requests.change_drifter_opmode_request import \
    ChangeDrifterOpModeRequest
from core.communication_system.domain.communicator.requests.change_localizer_opmode_request import \
    ChangeLocalizerOpModeRequest
from core.communication_system.domain.communicator.requests.ping_drifter_request import PingDrifterRequest
from core.communication_system.domain.communicator.requests.ping_localizer_request import \
    PingLocalizerRequest
from core.communication_system.domain.communicator.requests.ping_raspberry_request import \
    PingRaspberryRequest


class CommunicationSystemClient:
    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def ping_drifter(self) -> CommunicationResult:
        result = self.communicator.send_request(PingDrifterRequest())
        return result

    def ping_localizer(self) -> CommunicationResult:
        result = self.communicator.send_request(PingLocalizerRequest())
        return result

    def ping_raspberry(self) -> CommunicationResult:
        result = self.communicator.send_request(PingRaspberryRequest())
        return result

    def change_drifter_op_mode(self, op_mode: int) -> CommunicationResult:
        result = self.communicator.send_request(ChangeDrifterOpModeRequest(op_mode))
        return result

    def change_localizer_op_mode(self, op_mode: int) -> CommunicationResult:
        result = self.communicator.send_request(ChangeLocalizerOpModeRequest(op_mode))
        return result
