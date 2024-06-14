from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communication_responses.communication_response import CommunicationResponse
from apps.communication.iclisten_client.communicator.communicator import Communicator


class ICListenClient:
    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def send(self, request: CommunicationRequest) -> CommunicationResponse:
        response = self.communicator.send_request(request)
        return response

    def close(self):
        self.communicator.close()
