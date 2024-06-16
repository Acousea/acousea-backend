from apps.communication.communication_requests.ping_drifter_request.ping_drifter_request import PingDrifterRequest
from apps.communication.communication_responses.communication_response import CommunicationResponse
from apps.communication.communication_responses.ping_drifter_response.ping_drifter_response import PingDrifterResponse
from apps.communication.communicator.communicator import Communicator


class DrifterClient:
    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def ping(self) -> CommunicationResponse:
        response = self.communicator.send_request(PingDrifterRequest(), PingDrifterResponse)
        return response
